"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置类"""

    # App
    APP_NAME: str = "PetsPhoto"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./petsphoto.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # JWT
    JWT_SECRET_KEY: str = ""  # Will fall back to SECRET_KEY if not provided
    JWT_ALGORITHM: str = "HS256"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use SECRET_KEY as JWT_SECRET_KEY if not provided
        if not self.JWT_SECRET_KEY:
            self.JWT_SECRET_KEY = self.SECRET_KEY

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_JWT_SECRET: str = ""  # JWT Secret from Supabase project settings

    # Authentik (deprecated - keeping for backward compatibility)
    AUTHENTIK_DOMAIN: str = ""
    AUTHENTIK_CLIENT_ID: str = ""
    AUTHENTIK_CLIENT_SECRET: str = ""
    AUTHENTIK_REDIRECT_URI: str = ""

    # Image Generation API
    # 支持的提供商: mock, google_ai, stability_ai, replicate
    IMAGE_PROVIDER: str = "mock"

    # Google AI (Vertex AI - Imagen)
    GOOGLE_AI_API_KEY: str = ""
    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_LOCATION: str = "us-central1"  # Vertex AI 区域
    GOOGLE_BASE_URL_TEMPLATE: str = "https://{location}-aiplatform.googleapis.com/v1"  # Base URL 模板
    GOOGLE_MODEL: str = "publishers/google/models/gemini-2.5-flash-image"  # Gemini 2.5 Flash Image 模型
    GOOGLE_SERVICE_ACCOUNT_PATH: str = ""  # Service Account JSON 文件路径（可选）

    # Stability AI (Stable Diffusion)
    STABILITY_AI_API_KEY: str = ""
    STABILITY_AI_BASE_URL: str = "https://api.stability.ai"
    STABILITY_AI_MODEL: str = "stable-diffusion-xl-1024-v1-0"

    # Replicate
    REPLICATE_API_KEY: str = ""
    REPLICATE_BASE_URL: str = "https://api.replicate.com/v1"
    REPLICATE_MODEL: str = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"

    # OpenRouter
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-exp:free"  # 支持图像生成的模型

    # 保留旧的 Veo3 配置（向后兼容）
    VEO3_API_KEY: str = ""
    VEO3_API_URL: str = "https://api.veo3.example.com"

    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:5177",
        "http://localhost:3000"
    ]

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    TEMP_DIR: str = "./uploads/temp"
    MAX_FILE_SIZE: int = 10485760  # 10MB

    # Base URL for constructing image URLs
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
