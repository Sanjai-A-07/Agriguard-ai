import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.services.model_service import Prediction


class FakeModelService:
    """Stands in for the real model so tests need no TensorFlow or dataset."""

    def __init__(self, top="Tomato___Early_blight", conf=0.95, status="confident", available=True):
        self.top, self.conf, self.status, self._available = top, conf, status, available

    @property
    def available(self):
        return self._available

    def predict(self, batch):
        return Prediction(self.top, self.conf, 0.9, self.status, {self.top: self.conf})


@pytest.fixture
def client():
    with TestClient(app) as c:
        app.state.model_service = FakeModelService()
        yield c


@pytest.fixture
def make_client():
    def _make(service):
        c = TestClient(app)
        c.__enter__()
        app.state.model_service = service
        return c
    return _make


def make_image_bytes(fmt="JPEG", size=(300, 300), textured=True) -> bytes:
    """Synthetic leaf-like test image (random texture so it passes the blur check)."""
    rng = np.random.default_rng(0)
    if textured:
        arr = rng.integers(60, 200, (size[1], size[0], 3), dtype=np.uint8)
    else:
        arr = np.full((size[1], size[0], 3), 120, dtype=np.uint8)
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format=fmt)
    return buf.getvalue()


@pytest.fixture
def jpeg_bytes():
    return make_image_bytes("JPEG")
