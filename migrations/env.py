# migrations/env.py
from sqlalchemy import create_engine
from alembic import context
from app.config import settings
from app.db.base import Base

target_metadata = Base.metadata

def run_migrations_online():
    # Use synchronous engine for Alembic
    connectable = create_engine(
        settings.database_url.replace("aiosqlite", "pysqlite"),
        connect_args={"check_same_thread": False}  # SQLite needs this
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    url = settings.database_url
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()
