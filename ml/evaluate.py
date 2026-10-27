"""Evaluate on the held-out test set. All numbers are measured, never assumed.

Usage:  python ml/evaluate.py --data data/tomato_split
Writes models/evaluation.json and models/confusion_matrix.png.
Also prints how many predictions would be flagged "uncertain" at several
confidence thresholds, to help you choose CONFIDENCE_THRESHOLD from VALIDATION data.
NOTE: PlantVillage images are lab-style photos; these scores will likely overstate
performance on real field photographs. Evaluate field images separately if you have them.
"""
import argparse, json, time
from pathlib import Path
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix


def collect(model, ds):
    y, probs = [], []
    for xb, yb in ds:
        probs.append(model.predict(xb, verbose=0)); y.append(np.argmax(yb.numpy(), 1))
    return np.concatenate(y), np.concatenate(probs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=Path("data/tomato_split"))
    ap.add_argument("--models", type=Path, default=Path("models"))
    a = ap.parse_args()

    names = json.loads((a.models / "class_names.json").read_text())
    model = tf.keras.models.load_model(a.models / "crop_disease.keras", compile=False)
    load = lambda s: tf.keras.utils.image_dataset_from_directory(
        a.data / s, image_size=(224, 224), batch_size=32, label_mode="categorical", shuffle=False)
    test, val = load("test"), load("val")
    assert test.class_names == names, "Class order differs from class_names.json"

    y, p = collect(model, test)
    pred = p.argmax(1)
    rep = classification_report(y, pred, target_names=names, output_dict=True, zero_division=0)
    cm = confusion_matrix(y, pred)

    one = next(iter(test.unbatch().batch(1).take(1)))[0]
    model.predict(one, verbose=0)  # warm-up
    t = time.perf_counter()
    for _ in range(30): model.predict(one, verbose=0)
    latency_ms = (time.perf_counter() - t) / 30 * 1000

    yv, pv = collect(model, val)
    sweep = {}
    for th in [0.5, 0.6, 0.7, 0.8, 0.9, 0.95]:
        keep = pv.max(1) >= th
        sweep[str(th)] = {
            "coverage": float(keep.mean()),
            "accuracy_on_kept": float((pv.argmax(1)[keep] == yv[keep]).mean()) if keep.any() else None,
        }

    out = {
        "test_images": int(len(y)),
        "accuracy": float((pred == y).mean()),
        "macro_precision": rep["macro avg"]["precision"],
        "macro_recall": rep["macro avg"]["recall"],
        "macro_f1": rep["macro avg"]["f1-score"],
        "per_class": {n: rep[n] for n in names},
        "confusion_matrix": cm.tolist(),
        "latency_ms_single_image_cpu_avg": latency_ms,
        "validation_threshold_sweep": sweep,
    }
    (a.models / "evaluation.json").write_text(json.dumps(out, indent=2))

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(cm, cmap="Greens"); ax.set_xticks(range(len(names))); ax.set_yticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right"); ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(len(names)):
            ax.text(j, i, cm[i, j], ha="center", va="center")
    ax.set_xlabel("Predicted"); ax.set_ylabel("True"); fig.tight_layout()
    fig.savefig(a.models / "confusion_matrix.png", dpi=120)
    print(json.dumps({k: out[k] for k in ["test_images", "accuracy", "macro_f1", "latency_ms_single_image_cpu_avg"]}, indent=2))
    print("Threshold sweep (validation):", json.dumps(sweep, indent=2))


if __name__ == "__main__":
    main()
