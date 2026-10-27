from typing import Literal, Optional
from pydantic import BaseModel

PredictionStatus = Literal["confident", "uncertain", "poor_image"]


class HealthResponse(BaseModel):
    status: str
    model_available: bool


class CropInfo(BaseModel):
    id: str
    name: str
    classes: list[str]


class Guidance(BaseModel):
    class_name: str
    crop: str
    disease_name: str
    is_healthy: bool
    symptoms: list[str]
    prevention: list[str]
    management_guidance: list[str]
    next_steps: list[str]
    sources: list[str]
    last_reviewed: Optional[str]
    review_status: str


class ImageQuality(BaseModel):
    sharpness: float
    brightness: float
    warnings: list[str]


class PredictionResponse(BaseModel):
    scan_id: str
    crop: str
    predicted_class: Optional[str]
    top_prediction: str
    confidence: float
    status: PredictionStatus
    message: str
    image_quality: ImageQuality
    guidance: Optional[Guidance]
    disclaimer: str


class ErrorResponse(BaseModel):
    error: str
    detail: str
