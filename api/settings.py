from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class APISettings(BaseSettings):
    # API configuration
    API_PREFIX: str = "/v1"
    MAX_INPUT_CHARS: int = 10000  # Default to 10k chars to prevent abuse, yet allow large PDFs
    REQUEST_TIMEOUT_SECONDS: int = 500  # 500s timeout (must be > 465s worst-case LLM retry)
    
    # CORS Configuration
    # Example format: 'http://localhost:3000,http://127.0.0.1:3000'
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # File upload settings
    MAX_UPLOAD_SIZE_MB: int = 25
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ALLOWED_ORIGINS.split(",") if o.strip()]

settings = APISettings()
