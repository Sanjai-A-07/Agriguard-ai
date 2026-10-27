import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.errors import AppError
from app.routes import advice, crops, predict
from app.schemas import HealthResponse
from app.services.model_service import ModelService

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("agriguard")


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = ModelService(get_settings())
    service.load()  # once, at startup
    app.state.model_service = service
    yield


app = FastAPI(title="AgriGuard AI", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origin_list,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.error, "detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": "validation_error", "detail": "The request was missing or had invalid fields (for example, no image was attached)."})


@app.exception_handler(Exception)
async def unhandled_handler(_: Request, exc: Exception):
    log.exception("Unhandled error")  # log the stack trace, not the user's data
    return JSONResponse(status_code=500, content={"error": "server_error", "detail": "Something went wrong on our side. Please try again."})


@app.get("/health", response_model=HealthResponse)
def health(request: Request):
    return HealthResponse(status="ok", model_available=request.app.state.model_service.available)


app.include_router(crops.router)
app.include_router(advice.router)
app.include_router(predict.router)
