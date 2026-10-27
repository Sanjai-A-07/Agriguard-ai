"""Build train/val/test splits from a PlantVillage checkout.

Usage:
    python ml/prepare_dataset.py --source <PlantVillage-Dataset>/raw/color --out data/tomato_split

- Lists the tomato class folders it actually finds, and aborts if any wanted class is missing.
- Drops unreadable images (reported in the output).
- Groups exact duplicates (content hash) and PlantVillage augmentation variants
  (names ending _flipLR, _flipTB, _new30degFlipLR, ...) so a group never spans two splits.
  This catches identifiable duplicates only; it cannot prove the splits are fully independent.
"""
import argparse, hashlib, json, random, re, shutil
from collections import defaultdict
from pathlib import Path
from PIL import Image

WANTED = [
    "Tomato___healthy", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Bacterial_spot", "Tomato___Leaf_Mold",
]
EXTS = {".jpg", ".jpeg", ".png"}
VARIANT = re.compile(r"(_flip(LR|TB)|_new\d+deg\w*|_\d+deg\w*)$", re.I)


def base_key(path: Path) -> str:
    return VARIANT.sub("", path.stem)


def is_valid(path: Path) -> bool:
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
        return True
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--out", default=Path("data/tomato_split"), type=Path)
    ap.add_argument("--val", type=float, default=0.15)
    ap.add_argument("--test", type=float, default=0.15)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()

    found = sorted(p.name for p in a.source.iterdir() if p.is_dir() and p.name.lower().startswith("tomato"))
    print("Tomato folders found:", *found, sep="\n  ")
    missing = [c for c in WANTED if c not in found]
    if missing:
        raise SystemExit(f"Missing expected class folders: {missing}. Update WANTED to match the dataset.")

    rng = random.Random(a.seed)
    report = {"classes": {}, "corrupted": []}
    if a.out.exists():
        shutil.rmtree(a.out)

    for cls in WANTED:
        files = [p for p in (a.source / cls).iterdir() if p.suffix.lower() in EXTS]
        groups: dict[str, list[Path]] = defaultdict(list)
        seen_hash: dict[str, str] = {}
        for p in files:
            if not is_valid(p):
                report["corrupted"].append(str(p)); continue
            h = hashlib.md5(p.read_bytes()).hexdigest()
            key = seen_hash.setdefault(h, base_key(p))  # identical bytes -> same group
            groups[key].append(p)
        keys = sorted(groups); rng.shuffle(keys)
        n = len(keys); n_test = int(n * a.test); n_val = int(n * a.val)
        split_keys = {"test": keys[:n_test], "val": keys[n_test:n_test + n_val], "train": keys[n_test + n_val:]}
        counts = {}
        for split, ks in split_keys.items():
            dest = a.out / split / cls
            dest.mkdir(parents=True, exist_ok=True)
            c = 0
            for k in ks:
                for p in groups[k]:
                    shutil.copy2(p, dest / p.name); c += 1
            counts[split] = c
        report["classes"][cls] = counts
        print(cls, counts)

    (a.out / "split_report.json").write_text(json.dumps(report, indent=2))
    print(f"Corrupted files skipped: {len(report['corrupted'])}")


if __name__ == "__main__":
    main()
