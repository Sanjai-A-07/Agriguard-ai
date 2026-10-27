from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    model_path: str = "../models/crop_disease.keras"
    class_names_path: str = "../models/class_names.json"
    cors_origins: str = "http://localhost:5173"
    max_upload_size_mb: int = 5
    max_image_dimension: int = 6000
    min_image_dimension: int = 64
    confidence_threshold: float = 0.80
    min_margin: float = 0.20
    blur_threshold: float = 60.0
    input_size: int = 224

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
