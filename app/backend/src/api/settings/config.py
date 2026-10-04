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
    return url.set(drivername="postgresql+asyncpg")


DATABASE_URL = async_database_url(DATABASE_URL)
