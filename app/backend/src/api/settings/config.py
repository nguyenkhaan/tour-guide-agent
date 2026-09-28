"""
Application settings loaded from environment variables.
All sensitive values (keys, URLs, passwords) MUST live in .env — never hardcoded here.
"""
import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file if it exists


class _NoArg:
    """A sentinel value to indicate that a parameter was not given"""


NO_ARG = _NoArg()


def get_env_var(key: str, default: str | _NoArg = NO_ARG) -> str:
    """Get an environment variable, raise an error if it is missing and no default is given."""
    try:
        return os.environ[key]
    except KeyError:
        if isinstance(default, _NoArg):
            raise ValueError(f"Environment variable {key} is missing")
        return default


# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL: str = get_env_var("DATABASE_URL")

# ── JWT / Auth ────────────────────────────────────────────────────────────────
JWT_SECRET_KEY: str = get_env_var("JWT_SECRET_KEY")
JWT_ALGORITHM: str = get_env_var("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(get_env_var("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

# ── MinIO / Object Storage ────────────────────────────────────────────────────
MINIO_ENDPOINT: str = get_env_var("MINIO_ENDPOINT", "localhost:9000")
MINIO_ROOT_USER: str = get_env_var("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD: str = get_env_var("MINIO_ROOT_PASSWORD")
MINIO_BUCKET_NAME: str = get_env_var("MINIO_BUCKET_NAME", "tour-guide-media")
MINIO_USE_SSL: bool = get_env_var("MINIO_USE_SSL", "false").lower() == "true"

# ── Application ───────────────────────────────────────────────────────────────
APP_ENV: str = get_env_var("APP_ENV", "development")
APP_DEBUG: bool = get_env_var("APP_DEBUG", "false").lower() == "true"

# ── Conventions (Phase 2 Standards) ──────────────────────────────────────────
# All monetary values stored as NUMERIC(15,2) in VND; other currencies use VARCHAR(3)
DEFAULT_CURRENCY: str = get_env_var("DEFAULT_CURRENCY", "VND")

# All datetime values stored as TIMESTAMPTZ (timezone-aware UTC).
# Displayed to users in APP_TIMEZONE.
APP_TIMEZONE: str = get_env_var("APP_TIMEZONE", "Asia/Ho_Chi_Minh")