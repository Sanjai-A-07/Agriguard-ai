"""Train a MobileNetV2 transfer-learning classifier.

Usage:  python ml/train.py --data data/tomato_split --epochs 15 --finetune-epochs 5

MobileNetV2 preprocessing (scale pixels to [-1, 1]) is built INTO the saved model, so
the backend feeds raw 0-255 pixels and cannot drift from training. Augmentation layers
are only active during training.
"""
import argparse, json
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers

SIZE = 224


def load(data: Path, split: str, batch: int, shuffle: bool):
    return tf.keras.utils.image_dataset_from_directory(
        data / split, image_size=(SIZE, SIZE), batch_size=batch,
        label_mode="categorical", shuffle=shuffle, seed=42,
    )


def build(num_classes: int):
    inputs = layers.Input((SIZE, SIZE, 3))
    x = layers.RandomFlip("horizontal_and_vertical")(inputs)
    x = layers.RandomRotation(0.15)(x)
    x = layers.RandomZoom(0.15)(x)
    x = layers.RandomBrightness(0.2, value_range=(0, 255))(x)
    x = layers.Rescaling(1 / 127.5, offset=-1)(x)  # == mobilenet_v2.preprocess_input
    base = tf.keras.applications.MobileNetV2(input_shape=(SIZE, SIZE, 3), include_top=False, weights="imagenet")
    base.trainable = False
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
    return tf.keras.Model(inputs, outputs), base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=Path("data/tomato_split"))
    ap.add_argument("--out", type=Path, default=Path("models"))
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--finetune-epochs", type=int, default=0)
    a = ap.parse_args()
    a.out.mkdir(exist_ok=True)

    train, val = load(a.data, "train", a.batch, True), load(a.data, "val", a.batch, False)
    class_names = train.class_names
    (a.out / "class_names.json").write_text(json.dumps(class_names, indent=2))
    prefetch = lambda d: d.prefetch(tf.data.AUTOTUNE)
    train, val = prefetch(train), prefetch(val)

    model, base = build(len(class_names))
    ckpt = str(a.out / "crop_disease.keras")
    cbs = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(ckpt, monitor="val_loss", save_best_only=True),
    ]
    model.compile(tf.keras.optimizers.Adam(1e-3), "categorical_crossentropy", metrics=["accuracy"])
    h1 = model.fit(train, validation_data=val, epochs=a.epochs, callbacks=cbs)
    history = {k: list(map(float, v)) for k, v in h1.history.items()}

    if a.finetune_epochs:
        base.trainable = True
        for layer in base.layers[:-30]:  # unfreeze only the top ~30 layers
            layer.trainable = False
        model.compile(tf.keras.optimizers.Adam(1e-5), "categorical_crossentropy", metrics=["accuracy"])
        h2 = model.fit(train, validation_data=val, epochs=a.finetune_epochs, callbacks=cbs)
        for k, v in h2.history.items():
            history[k] += list(map(float, v))

    model.save(ckpt)  # best weights were restored by EarlyStopping
    (a.out / "history.json").write_text(json.dumps(history))

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for i, m in enumerate(["accuracy", "loss"]):
        ax[i].plot(history[m], label="train"); ax[i].plot(history[f"val_{m}"], label="validation")
        ax[i].set_title(m); ax[i].set_xlabel("epoch"); ax[i].legend()
    fig.tight_layout(); fig.savefig(a.out / "training_curves.png", dpi=120)
    print("Saved", ckpt)


if __name__ == "__main__":
    main()
