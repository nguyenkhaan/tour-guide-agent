import os

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy.engine import make_url

load_dotenv(Path(__file__).resolve().parents[3] / ".env")  # Load environment variables from .env file if it exists


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


DATABASE_URL = get_env_var("DATABASE_URL")


def async_database_url(value: str):
    url = make_url(value)
    if url.get_backend_name() != "postgresql":
        raise ValueError("DATABASE_URL must point to PostgreSQL with PostGIS")
    query = dict(url.query)
    query.pop("channel_binding", None)
    if "sslmode" in query:
        ssl_val = query.pop("sslmode")
        query["ssl"] = ssl_val if ssl_val != "prefer" else "require"

    return url.set(drivername="postgresql+asyncpg", query=query)


DATABASE_URL = async_database_url(DATABASE_URL)

JWT_ACCESS_SECRET_KEY = get_env_var("JWT_ACCESS_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = get_env_var("JWT_REFRESH_SECRET_KEY")
JWT_ALGORITHM = get_env_var("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # Default 24 hours
REFRESH_TOKEN_EXPIRE_MINUTES = int(get_env_var("REFRESH_TOKEN_EXPIRE_MINUTES"))
