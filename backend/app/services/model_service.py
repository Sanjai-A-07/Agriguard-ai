"""Loads the trained model once and turns raw probabilities into a safe result."""
import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from app.config import Settings

log = logging.getLogger("agriguard.model")


@dataclass
class Prediction:
    top_class: str
    confidence: float
    margin: float
    status: str  # confident | uncertain
    probabilities: dict[str, float]


class ModelService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model = None
        self.class_names: list[str] = []

    @property
    def available(self) -> bool:
        return self.model is not None and bool(self.class_names)

    def load(self) -> None:
        model_path = Path(self.settings.model_path)
        names_path = Path(self.settings.class_names_path)
        if not model_path.exists() or not names_path.exists():
            log.warning("Model or class names not found; /api/predict will return 503.")
            return
        try:
            import tensorflow as tf  # imported lazily so tests run without TF

            self.model = tf.keras.models.load_model(model_path, compile=False)
            self.class_names = json.loads(names_path.read_text(encoding="utf-8"))
            log.info("Loaded model with %d classes", len(self.class_names))
        except Exception:
            log.exception("Failed to load model")
            self.model = None

    def _raw_predict(self, batch: np.ndarray) -> np.ndarray:
        return self.model.predict(batch, verbose=0)[0]

    def predict(self, batch: np.ndarray) -> Prediction:
        probs = self._raw_predict(batch)
        order = np.argsort(probs)[::-1]
        top, second = float(probs[order[0]]), float(probs[order[1]]) if len(probs) > 1 else 0.0
        margin = top - second
        confident = top >= self.settings.confidence_threshold and margin >= self.settings.min_margin
        return Prediction(
            top_class=self.class_names[int(order[0])],
            confidence=top,
            margin=margin,
            status="confident" if confident else "uncertain",
            probabilities={n: float(p) for n, p in zip(self.class_names, probs)},
        )
