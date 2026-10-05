# uv run python -m scripts.seed

import asyncio
import importlib
import json
import pkgutil
from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import src.models
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from sqlalchemy import Date, DateTime, Numeric, Time, UUID as SQLAlchemyUUID, select
from sqlalchemy.sql.schema import Column

from src.db import async_session_maker, engine
from src.models.base_model import Base


DATA_FILE = Path(__file__).with_name("data.json")


def load_models() -> None:
    for module in pkgutil.iter_modules(src.models.__path__):
        if module.name.endswith("_model") and module.name != "base_model":
            importlib.import_module(f"src.models.{module.name}")


def convert_value(column: Column[Any], value: Any) -> Any:
    if value is None:
        return None
    if isinstance(column.type, SQLAlchemyUUID):
        return UUID(value)
    if isinstance(column.type, DateTime):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(column.type, Date):
        return date.fromisoformat(value)
    if isinstance(column.type, Time):
        return time.fromisoformat(value)
    if isinstance(column.type, Numeric):
        return Decimal(str(value))
    if isinstance(column.type, Geometry):
        return WKTElement(value, srid=column.type.srid or 4326)
    return value


def prepare_rows(table: Any, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    columns = {column.name: column for column in table.columns}
    prepared = []
    for row in rows:
        unknown = set(row) - set(columns)
        if unknown:
            raise ValueError(f"Unknown columns for {table.name}: {sorted(unknown)}")
        prepared.append({name: convert_value(columns[name], value) for name, value in row.items()})
    return prepared


async def seed() -> None:
    load_models()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    tables = list(Base.metadata.sorted_tables)
    missing_tables = {table.name for table in tables} - set(data)
    unknown_tables = set(data) - {table.name for table in tables}
    if missing_tables or unknown_tables:
        raise ValueError(
            f"Seed table mismatch. Missing: {sorted(missing_tables)}; unknown: {sorted(unknown_tables)}"
        )

    required_users = {
        "admin@gmail.com": "ADMIN",
        "employee1@gmail.com": "OPERATOR",
        "employee2@gmail.com": "OPERATOR",
        "customer1@gmail.com": "USER",
        "customer2@gmail.com": "USER",
    }
    users = {user["email"]: user for user in data["users"]}
    for email, role in required_users.items():
        user = users.get(email)
        if not user or user["password"] != "user123" or user["role"] != role:
            raise ValueError(f"Required seed account is invalid: {email}")

    inserted = 0
    async with async_session_maker() as session:
        async with session.begin():
            for table in tables:
                if await session.scalar(select(1).select_from(table).limit(1)) is not None:
                    raise RuntimeError(f"Seed aborted: table '{table.name}' already contains data")
            for table in tables:
                rows = prepare_rows(table, data[table.name])
                if rows:
                    await session.execute(table.insert(), rows)
                    inserted += len(rows)

    print(f"Seeded {inserted} records across {len(tables)} tables.")


async def main() -> None:
    try:
        await seed()
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
