from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.core.config import settings
from app.core.database import Base
import app.models  # ensures models are registered on Base.metadata
import os

# Ensure project root is on sys.path so `app` package imports work
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load .env if present and ensure minimal env vars exist so Settings() can initialize
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except Exception:
    pass

os.environ.setdefault("PAYSTACK_SECRET_KEY", "")
os.environ.setdefault("PAYSTACK_PUBLIC_KEY", "")
os.environ.setdefault("JWT_SECRET_KEY", "alembic-placeholder-key")



config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Pull URL from your app settings (.env), not hardcoded alembic.ini
db_url = settings.DATABASE_URL
# configparser treats '%' specially; escape them so URLs with '%' work
db_url_escaped = db_url.replace('%', '%%')
config.set_main_option("sqlalchemy.url", db_url_escaped)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())