from fastapi import APIRouter

from app.schemas import CropInfo
from app.services import advice_service

router = APIRouter(prefix="/api")


@router.get("/crops", response_model=list[CropInfo])
def list_crops():
    return [
        CropInfo(id=cid, name=name, classes=advice_service.classes_for_crop(cid))
        for cid, name in advice_service.SUPPORTED_CROPS.items()
    ]
