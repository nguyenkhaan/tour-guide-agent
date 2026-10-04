import argparse
import ast
import asyncio
from collections import Counter
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from enum import Enum
from io import StringIO
from pathlib import Path
import re
import subprocess
import tokenize
import unittest
from uuid import uuid4

from alembic import command
from alembic.config import Config
from geoalchemy2 import Geometry
import sqlalchemy as sa
from pydantic import TypeAdapter
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import configure_mappers

from src.models import Base, Users, UserProfile, AgentSession, MediaFiles
from src.models import base_model

ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT.parent.parent / "docs/DATABASE.txt").read_text(encoding="utf-8")
SPEC = {}
for name, body in re.findall(r"table\s+(\w+)\s*\{([^}]+)\}", SOURCE):
    SPEC[name] = {}
    for line in body.splitlines():
        declaration = line.split("//", 1)[0].strip()
        if declaration:
            field, kind, *flags = declaration.split()
            SPEC[name][field] = (kind, flags)


def alembic_config():
    return Config(str(ROOT / "alembic.ini"))


class ModelChecks(unittest.TestCase):
    def test_existing_comments_preserved_and_new_comments_match_database(self):
        allowed = {line.split("//", 1)[1].strip()
                   for line in SOURCE.splitlines() if "//" in line}
        repository = ROOT.parent.parent

        def comments(content):
            return Counter(token.string.rstrip() for token in tokenize.generate_tokens(StringIO(content).readline)
                           if token.type == tokenize.COMMENT)

        def docstrings(content):
            return Counter(value for node in ast.walk(ast.parse(content))
                           if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
                           and (value := ast.get_docstring(node, clean=False)) is not None)

        paths = list((ROOT / "src/models").glob("*.py"))
        paths += list((ROOT / "alembic").rglob("*.py"))
        paths += [ROOT / "src/db.py", ROOT / "src/app.py",
                  ROOT / "src/api/settings/config.py", Path(__file__)]
        for path in paths:
            content = path.read_text(encoding="utf-8")
            relative = path.resolve().relative_to(repository).as_posix()
            result = subprocess.run(["git", "show", f"dev:{relative}"], cwd=repository,
                                    capture_output=True, text=True, encoding="utf-8")
            previous = result.stdout if result.returncode == 0 else ""
            with self.subTest(file=path.name):
                self.assertFalse(comments(previous) - comments(content), "Existing comments were removed")
                self.assertEqual(docstrings(content), docstrings(previous))
                for comment in comments(content) - comments(previous):
                    self.assertEqual(path.parent, ROOT / "src/models")
                    self.assertIn(comment.removeprefix("#").strip(), allowed)

        for relative in (".gitignore", "app/backend/.gitignore"):
            previous = subprocess.check_output(["git", "show", f"dev:{relative}"], cwd=repository).decode("utf-8")
            current = (repository / relative).read_text(encoding="utf-8")
            old_comments = Counter(line.rstrip() for line in previous.splitlines() if line.lstrip().startswith("#"))
            new_comments = Counter(line.rstrip() for line in current.splitlines() if line.lstrip().startswith("#"))
            self.assertEqual(new_comments, old_comments)

    def test_registered_tables_match_database_specification(self):
        self.assertEqual(set(Base.metadata.tables), set(SPEC))
        self.assertNotIn("todo", Base.metadata.tables)

    def test_source_does_not_contain_private_keys_tokens_or_local_env_secrets(self):
        from dotenv import dotenv_values
        repository = ROOT.parent.parent
        values = dotenv_values(ROOT / ".env")
        secrets = [str(value) for key, value in values.items()
                   if value and re.search(r"(?i)(key|secret|token|password|pass$|database_url)", key)
                   and len(str(value)) >= 12]
        signatures = [
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
            re.compile(r"\b(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{24,}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{20,})\b"),
        ]
        paths = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=repository).decode().split("\0")
        for relative in sorted(set(filter(None, paths))):
            path = repository / relative
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                continue

            self.assertFalse(any(pattern.search(content) for pattern in signatures),
                             f"Potential private key/provider token in {relative}")
            self.assertFalse(any(secret in content for secret in secrets),
                             f"Local environment secret copied into {relative}")

    def test_secret_files_are_ignored_and_untracked(self):
        repository = ROOT.parent.parent
        paths = [".env", ".env.local", ".env.production", ".env.backup",
                 "app/backend/.env", "app/backend/.env.test", "app/frontend/.env.local",
                 "secrets.json", "credentials.json", "private.key", "server.pem",
                 ".aws/credentials", ".ssh/id_rsa", "secrets/api.json"]
        for path in paths:
            with self.subTest(path=path):
                result = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=repository)
                self.assertEqual(result.returncode, 0)
                tracked = subprocess.check_output(["git", "ls-files", "--", path], cwd=repository).decode().strip()
                self.assertEqual(tracked, "", "A sensitive file is already tracked; .gitignore alone cannot protect it")

    def test_datetime_representation(self):
        local = datetime(2026, 10, 4, 10, tzinfo=timezone(timedelta(hours=7)))
        self.assertEqual(base_model.datetime_to_iso8601(local), "2026-10-04T03:00:00Z")
        with self.assertRaises(ValueError):
            base_model.as_utc(datetime(2026, 10, 4, 10))

    def test_all_tables_columns_primary_keys_and_files_match_source(self):
        configure_mappers()
        self.assertEqual(set(Base.metadata.tables), set(SPEC))
        for name, fields in SPEC.items():
            with self.subTest(table=name):
                table = Base.metadata.tables[name]
                self.assertEqual(set(table.columns.keys()), set(fields))
                self.assertEqual(set(table.primary_key.columns.keys()),
                                 {field for field, (_, flags) in fields.items() if "PK" in flags})
                tree = ast.parse((ROOT / f"src/models/{name}_model.py").read_text(encoding="utf-8"))
                self.assertEqual(sum(isinstance(node, ast.ClassDef) for node in tree.body), 1)

    def test_every_declared_column_type_matches(self):
        for table_name, fields in SPEC.items():
            for name, (kind, _) in fields.items():
                with self.subTest(table=table_name, column=name):
                    type_ = Base.metadata.tables[table_name].c[name].type
                    upper = kind.upper()
                    if upper.startswith("VARCHAR"):
                        self.assertIsInstance(type_, sa.String)
                        self.assertEqual(type_.length, int(re.search(r"\d+", kind).group()))
                    elif upper.startswith("NUMERIC"):
                        self.assertIsInstance(type_, sa.Numeric)
                        precision, scale = map(int, re.findall(r"\d+", kind))
                        self.assertEqual((type_.precision, type_.scale), (precision, scale))
                    elif upper.startswith("GEOMETRY"):
                        self.assertIsInstance(type_, Geometry)
                        self.assertEqual((type_.geometry_type, type_.srid), ("POINT", 4326))
                    elif upper == "TIMESTAMP":
                        self.assertIsInstance(type_, sa.DateTime)
                        self.assertTrue(type_.timezone)
                    elif upper == "TIME":
                        self.assertIsInstance(type_, sa.Time)
                        self.assertFalse(type_.timezone)
                    elif upper == "UUID": self.assertIsInstance(type_, sa.UUID)
                    elif upper == "JSONB": self.assertIsInstance(type_, postgresql.JSONB)
                    elif upper == "DATE": self.assertIsInstance(type_, sa.Date)
                    elif upper == "BIGINT": self.assertIsInstance(type_, sa.BigInteger)
                    elif upper in ("INT", "SERIAL"): self.assertIsInstance(type_, sa.Integer)
                    elif upper == "FLOAT": self.assertIsInstance(type_, sa.Float)
                    elif upper == "BOOLEAN": self.assertIsInstance(type_, sa.Boolean)
                    elif kind == "TEXT": self.assertIsInstance(type_, sa.Text)
                    elif kind == "string": self.assertIsInstance(type_, sa.String)
                    else:
                        enum_class = getattr(base_model, kind)
                        self.assertIsInstance(type_, sa.Enum)
                        self.assertIs(type_.enum_class, enum_class)

    def test_enums_are_shared_str_types_for_orm_and_pydantic(self):
        tree = ast.parse((ROOT / "src/models/base_model.py").read_text(encoding="utf-8"))
        class_names = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
        enum_classes = {
            name: value for name, value in vars(base_model).items()
            if isinstance(value, type) and value is not Enum and issubclass(value, Enum)
        }
        self.assertEqual(class_names, {"Base", *enum_classes})

        for enum_class in enum_classes.values():
            self.assertTrue(issubclass(enum_class, str))
            self.assertTrue(issubclass(enum_class, Enum))
            values = [member.value for member in enum_class]

            database_type = Base.registry.type_annotation_map[enum_class]
            self.assertIsInstance(database_type, postgresql.ENUM)
            self.assertEqual(database_type.enums, values)
            self.assertTrue(database_type.validate_strings)

            adapter = TypeAdapter(enum_class)
            self.assertIs(adapter.validate_python(values[0]), enum_class(values[0]))
            self.assertEqual(adapter.dump_json(enum_class(values[0])), f'"{values[0]}"'.encode())

        for name, body in re.findall(r"enum\s+(\w+)\s*\{([^}]+)\}", SOURCE):
            values = re.findall(r"\b[A-Z][A-Z_]*\b", body)
            enum_class = getattr(base_model, name)
            self.assertEqual([member.value for member in enum_class], values)

    def test_foreign_keys_indexes_and_shared_conventions(self):
        self.assertEqual(next(iter(UserProfile.__table__.c.user_id.foreign_keys)).target_fullname, "users.id")
        self.assertTrue(Users.__table__.c.email.unique)
        self.assertTrue(Base.metadata.tables["places"].c.slug.unique)
        for table in Base.metadata.tables.values():
            for foreign_key in table.foreign_keys:
                target = foreign_key.column
                self.assertIsNotNone(target)
                column = foreign_key.parent
                self.assertTrue(column.primary_key or any(column in list(index.columns) for index in table.indexes))
            for constraint in table.constraints:
                self.assertIsNotNone(constraint.name)
                self.assertNotIn("`", constraint.name)
        self.assertNotIn("id", UserProfile.__table__.c)
        self.assertNotIn("id", Base.metadata.tables["system_configs"].c)
        self.assertEqual(Base.metadata.tables["messages"].c.metadata.name, "metadata")

    def test_offline_upgrade_and_downgrade_are_complete(self):
        buffer = StringIO()
        config = alembic_config()
        config.output_buffer = buffer
        command.upgrade(config, "head", sql=True)
        sql = buffer.getvalue()
        for table in SPEC:
            self.assertIn(f"CREATE TABLE {table} (", sql)
        self.assertIn("CREATE EXTENSION IF NOT EXISTS postgis", sql)
        self.assertIn("USING location::geometry", sql)
        enum_count = sum(
            isinstance(type_, postgresql.ENUM)
            for type_ in Base.registry.type_annotation_map.values()
        )
        self.assertEqual(sql.count("CREATE TYPE "), enum_count)
        self.assertNotIn("DROP TABLE todo", sql)
        buffer.seek(0)
        buffer.truncate(0)
        command.downgrade(config, "head:base", sql=True)
        sql = buffer.getvalue()
        for table in SPEC:
            self.assertIn(f"DROP TABLE {table}", sql)
        self.assertEqual(sql.count("DROP TYPE "), enum_count)


async def database_checks():
    from src.api.settings.config import DATABASE_URL
    import src.db as db
    schema = "phase2_test_" + uuid4().hex
    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True, hide_parameters=True,
        connect_args={
            "server_settings": {"timezone": "UTC", "search_path": f"{schema},public"},
            "timeout": 10,

            "prepared_statement_cache_size": 0,
            "statement_cache_size": 0,
            "prepared_statement_name_func": lambda: "__phase2_" + uuid4().hex,
        })
    @sa.event.listens_for(engine.sync_engine, "begin")
    def set_test_search_path(connection):

        connection.exec_driver_sql(f'SET LOCAL search_path TO "{schema}", public')
        connection.exec_driver_sql("SET LOCAL timezone TO 'UTC'")
    original_maker = db.async_session_maker


    db.async_session_maker = async_sessionmaker(
        engine.execution_options(schema_translate_map={None: schema}), expire_on_commit=False)
    schema_created = False
    try:
        async with engine.begin() as connection:
            await connection.execute(sa.text(f'CREATE SCHEMA "{schema}"'))
            schema_created = True
        engine.sync_engine.dialect.default_schema_name = schema
        async with engine.begin() as connection:
            def upgrade(sync_connection):
                config = alembic_config()
                config.attributes["connection"] = sync_connection
                config.attributes["version_table_schema"] = schema
                command.upgrade(config, "head")
            def bootstrap(sync_connection):
                config = alembic_config()
                config.attributes["connection"] = sync_connection
                config.attributes["version_table_schema"] = schema
                command.upgrade(config, "58f3a357343b")
                sync_connection.execute(sa.text("""INSERT INTO places (id, name, location)
                    VALUES (:id, 'Legacy place', ST_SetSRID(ST_MakePoint(106.7, 10.8), 4326)::geography)"""),
                    {"id": uuid4()})
                command.upgrade(config, "head")
            await connection.run_sync(bootstrap)
        print("PASS: real database upgrade from base to head")
        async with engine.connect() as connection:
            version = await connection.scalar(sa.text("SELECT version_num FROM alembic_version"))
            assert version == "20261004_phase2", version
            coordinates = (await connection.execute(sa.text("SELECT ST_X(location), ST_Y(location) FROM places WHERE name = 'Legacy place'"))).one()
            assert coordinates == (106.7, 10.8), coordinates
            def check(sync_connection):
                config = alembic_config()
                config.attributes["connection"] = sync_connection
                config.attributes["version_table_schema"] = schema
                local_tables = set(sa.inspect(sync_connection).get_table_names(schema=schema))
                config.attributes["include_name"] = lambda name, kind, parents: kind != "table" or (name in local_tables and name != "alembic_version")
                command.check(config)
            await connection.run_sync(check)
        print("PASS: Alembic reports no drift between migrated database and models")

        user_id = uuid4()
        async with db.transaction() as session:
            user = Users(id=user_id, email=f"{user_id}@phase2.test", password="hashed-placeholder",
                         status="ACTIVE", role="USER")
            session.add(user)
            await session.flush()
            session.add(UserProfile(user_id=user_id, default_budget=Decimal("123456.78"),
                                    preferred_currency="VND", travel_preferences={"food": True}))
            session.add(AgentSession(user_id=str(user_id), title="Acceptance test", status="ACTIVE"))
            session.add(MediaFiles(user_id=user_id, purpose="REQUEST_IMAGE", object_key="test/image.jpg"))
        async with db.transaction() as session:
            user = await session.get(Users, user_id)
            assert user is not None
            assert user.created_at.tzinfo is not None
            assert user.created_at.utcoffset().total_seconds() == 0
            profile = await session.get(UserProfile, user_id)
            assert profile.default_budget == Decimal("123456.78")
            assert profile.travel_preferences == {"food": True}
            purpose = await session.scalar(sa.select(MediaFiles.purpose).where(MediaFiles.user_id == user_id))
            assert purpose == "REQUEST_IMAGE"
            previous_updated_at = user.updated_at
            user.full_name = "Updated name"
        async with db.transaction() as session:
            user = await session.get(Users, user_id)
            assert user.full_name == "Updated name"
            assert user.updated_at > previous_updated_at
        print("PASS: ORM account/profile/session persistence, commit, Decimal, JSONB and UTC")

        rollback_id = uuid4()
        try:
            async with db.transaction() as session:
                session.add(Users(id=rollback_id, email=f"{rollback_id}@phase2.test"))
                await session.flush()
                raise RuntimeError("intentional rollback")
        except RuntimeError:
            pass
        async with db.transaction() as session:
            assert await session.get(Users, rollback_id) is None
        print("PASS: transaction rolls back flushed writes on application error")

        failures = [
            Users(email=f"{user_id}@phase2.test"),
            Users(email="invalid-enum@phase2.test", status="INVALID"),
            UserProfile(user_id=uuid4()),
        ]
        for obj in failures:
            try:
                async with db.transaction() as session:
                    session.add(obj)
                    await session.flush()
            except (sa.exc.IntegrityError, sa.exc.StatementError):
                pass
            else:
                raise AssertionError(f"Invalid row accepted: {type(obj).__name__}")
        try:
            async with db.transaction() as session:
                profile = await session.get(UserProfile, user_id)
                profile.default_budget = Decimal("-1")
                await session.flush()
        except sa.exc.IntegrityError:
            pass
        else:
            raise AssertionError("Negative profile budget accepted")
        print("PASS: unique email, enum, FK and budget constraints reject invalid writes")

        try:
            async with db.transaction() as session:
                profile = await session.get(UserProfile, user_id)
                profile.preferred_currency = "vnd"
                await session.flush()
        except sa.exc.IntegrityError:
            pass
        else:
            raise AssertionError("Lowercase currency code accepted")
        async with db.transaction() as session:
            profile = await session.get(UserProfile, user_id)
            assert profile.default_budget == Decimal("123456.78")
            assert profile.preferred_currency == "VND"
        print("PASS: currency convention and rollback after constraint failures")

        async with engine.begin() as connection:
            def downgrade(sync_connection):
                config = alembic_config()
                config.attributes["connection"] = sync_connection
                config.attributes["version_table_schema"] = schema
                command.downgrade(config, "58f3a357343b")
            await connection.run_sync(downgrade)
            tables = await connection.run_sync(lambda c: sa.inspect(c).get_table_names(schema=schema))
            assert set(tables) == {"alembic_version", "places", "todo"}, tables
        print("PASS: downgrade restores historical tables")
        async with engine.begin() as connection:
            await connection.run_sync(upgrade)
        print("PASS: upgrade can run again after downgrade")
    finally:
        db.async_session_maker = original_maker
        if schema_created:
            async with engine.begin() as connection:

                await connection.execute(sa.text(f'DROP SCHEMA "{schema}" CASCADE'))
            print("Temporary acceptance schema removed")
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", action="store_true")
    args = parser.parse_args()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ModelChecks))
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.database:
        asyncio.run(database_checks())
    else:
        print("Database checks NOT RUN. Use --database to verify live migrations and transactions.")
