from fastapi import APIRouter

from app.errors import AppError
from app.schemas import Guidance
from app.services import advice_service

router = APIRouter(prefix="/api")


@router.get("/advice/{class_name}", response_model=Guidance)
def get_advice(class_name: str):
    entry = advice_service.get_advice(class_name)
    if entry is None:
        raise AppError(404, "unknown_class", f"No reviewed information is available for '{class_name}'.")
    return entry
