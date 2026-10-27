import json
from functools import lru_cache
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "disease_information.json"

SUPPORTED_CROPS = {"tomato": "Tomato"}


@lru_cache
def _load() -> dict[str, dict]:
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {e["class_name"]: e for e in raw["entries"]}


def get_advice(class_name: str) -> dict | None:
    return _load().get(class_name)


def classes_for_crop(crop: str) -> list[str]:
    return [c for c, e in _load().items() if e["crop"] == crop]
