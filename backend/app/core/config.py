from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pydantic import field_validator
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


class Settings(BaseSettings):
    """Application settings loaded from .env file."""
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/homeleads"
    
    # Paystack Configuration
    PAYSTACK_SECRET_KEY: str
    PAYSTACK_PUBLIC_KEY: str
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Configuration
    APP_NAME: str = "HomeLeads API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Environment & Server Configuration
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """Normalize DB URL for async SQLAlchemy usage.

        - Converts postgresql://... to postgresql+asyncpg://...
        - Converts sslmode to ssl for asyncpg compatibility
        - Removes channel_binding query param (not used by asyncpg)
        """
        if not isinstance(value, str):
            return value

        raw = value.strip()
        if raw.startswith("postgresql://"):
            raw = raw.replace("postgresql://", "postgresql+asyncpg://", 1)

        parts = urlsplit(raw)
        if parts.scheme == "postgresql+asyncpg":
            normalized_qs = []
            for key, val in parse_qsl(parts.query, keep_blank_values=True):
                key_lower = key.lower()
                if key_lower == "channel_binding":
                    continue
                if key_lower == "sslmode":
                    ssl_val = val.lower()
                    if ssl_val in {"disable", "allow", "prefer"}:
                        normalized_qs.append(("ssl", "false"))
                    else:
                        normalized_qs.append(("ssl", "require"))
                    continue
                normalized_qs.append((key, val))

            raw = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(normalized_qs), parts.fragment))

        return raw
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()