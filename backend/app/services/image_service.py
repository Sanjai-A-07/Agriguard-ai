"""Upload validation and preprocessing.

Preprocessing here only resizes and converts to an RGB float array in the 0-255
range. The MobileNetV2 scaling to [-1, 1] lives INSIDE the saved Keras model
(see ml/train.py), so training and inference cannot drift apart.
"""
import io
from dataclasses import dataclass

import numpy as np
from PIL import Image, UnidentifiedImageError

from app.errors import AppError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
Image.MAX_IMAGE_PIXELS = 50_000_000  # decompression-bomb guard


@dataclass
class ProcessedImage:
    array: np.ndarray  # shape (1, size, size, 3), float32, 0-255
    sharpness: float
    brightness: float
    warnings: list[str]


def _sharpness(gray: np.ndarray) -> float:
    """Variance of a Laplacian filter; low values mean a blurry image."""
    g = gray.astype(np.float32)
    lap = (
        -4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    )
    return float(lap.var())


def validate_and_preprocess(
    data: bytes,
    *,
    max_bytes: int,
    max_dim: int,
    min_dim: int,
    size: int,
    blur_threshold: float,
) -> ProcessedImage:
    if not data:
        raise AppError(400, "empty_upload", "The uploaded file is empty.")
    if len(data) > max_bytes:
        raise AppError(
            413, "file_too_large",
            f"The image is larger than {max_bytes // (1024 * 1024)} MB. Please upload a smaller image.",
        )

    try:
        probe = Image.open(io.BytesIO(data))
        fmt = probe.format
        probe.verify()  # detects truncation/corruption; invalidates the object
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError, SyntaxError, ValueError):
        raise AppError(
            400, "invalid_image",
            "This file is not a readable image. Please upload a JPEG, PNG or WebP photo.",
        )
    if fmt not in ALLOWED_FORMATS:
        raise AppError(
            415, "unsupported_type",
            "Unsupported image type. Please upload a JPEG, PNG or WebP image.",
        )

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except (OSError, SyntaxError, ValueError):
        raise AppError(400, "invalid_image", "The image file appears to be corrupted.")

    w, h = img.size
    if max(w, h) > max_dim:
        raise AppError(413, "image_too_large", f"Image dimensions exceed {max_dim}px. Please resize it.")
    if min(w, h) < min_dim:
        raise AppError(400, "image_too_small", f"Image is too small (minimum {min_dim}px).")

    img = img.convert("RGB")  # drops alpha / palette
    gray = np.asarray(img.convert("L"))
    sharp = _sharpness(gray)
    bright = float(gray.mean())

    warnings: list[str] = []
    if sharp < blur_threshold:
        warnings.append("blurry")
    if bright < 50:
        warnings.append("too_dark")
    elif bright > 220:
        warnings.append("too_bright")

    resized = img.resize((size, size), Image.BILINEAR)
    arr = np.asarray(resized, dtype=np.float32)[np.newaxis, ...]
    return ProcessedImage(arr, round(sharp, 1), round(bright, 1), warnings)
