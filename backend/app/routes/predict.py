import uuid

from fastapi import APIRouter, File, Form, Request, UploadFile

from app.config import get_settings
from app.errors import AppError
from app.schemas import ImageQuality, PredictionResponse
from app.services import advice_service, image_service

router = APIRouter(prefix="/api")

DISCLAIMER = (
    "This is a preliminary, image-based result from an AI model trained on a limited set of "
    "tomato leaf images. It is not a diagnosis and does not replace an agricultural expert. "
    "Confirm with your local agricultural officer before applying any treatment."
)

MESSAGES = {
    "confident": "The model found a likely match among the supported tomato leaf categories.",
    "uncertain": "Unable to identify reliably. Please upload a clearer image or consult an agricultural expert.",
    "poor_image": "The photo quality is too low for a reliable result. Please retake it in good, even light with the leaf in focus.",
}


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, image: UploadFile = File(...), crop: str = Form("tomato")):
    settings = get_settings()
    crop = crop.strip().lower()
    if crop not in advice_service.SUPPORTED_CROPS:
        raise AppError(400, "unsupported_crop", f"Crop '{crop}' is not supported. Supported: {', '.join(advice_service.SUPPORTED_CROPS)}.")

    model_service = request.app.state.model_service
    if not model_service.available:
        raise AppError(503, "model_unavailable", "The prediction model is not available right now. Please try again later.")

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    data = await image.read(max_bytes + 1)  # never read more than the limit + 1 byte
    processed = image_service.validate_and_preprocess(
        data,
        max_bytes=max_bytes,
        max_dim=settings.max_image_dimension,
        min_dim=settings.min_image_dimension,
        size=settings.input_size,
        blur_threshold=settings.blur_threshold,
    )

    pred = model_service.predict(processed.array)
    status = pred.status
    if processed.warnings and status == "confident":
        # A sharp, well-lit photo is a precondition for trusting the score.
        status = "poor_image"

    guidance = advice_service.get_advice(pred.top_class) if status == "confident" else None

    return PredictionResponse(
        scan_id=str(uuid.uuid4()),
        crop=crop,
        predicted_class=pred.top_class if status == "confident" else None,
        top_prediction=pred.top_class,
        confidence=round(pred.confidence, 4),
        status=status,
        message=MESSAGES[status],
        image_quality=ImageQuality(
            sharpness=processed.sharpness, brightness=processed.brightness, warnings=processed.warnings
        ),
        guidance=guidance,
        disclaimer=DISCLAIMER,
    )
