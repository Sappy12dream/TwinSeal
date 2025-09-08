# app/core/cleanup.py
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import pairing as crud_pairing
from app.db.session import async_session
from pathlib import Path
from app.config import settings
from datetime import datetime, timedelta

async def cleanup_expired_pairings():
    async with async_session() as db:
        await crud_pairing.delete_expired_pairing_ids(db)

async def cleanup_stale_files(days: int = 30):
    """Delete files older than `days` from storage and DB"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    from app.models.file import File
    async with async_session() as db:
        result = await db.execute(
            "SELECT * FROM files WHERE created_at <= :cutoff", {"cutoff": cutoff}
        )
        files = result.fetchall()
        for file in files:
            filepath = Path(settings.file_storage_path) / file.stored_filename
            if filepath.exists():
                filepath.unlink()
            await db.delete(file)
        await db.commit()

async def start_cleanup_loop(interval_seconds: int = 3600):
    """Run cleanup periodically in the background"""
    while True:
        try:
            await cleanup_expired_pairings()
            await cleanup_stale_files()
        except Exception as e:
            import logging
            logging.getLogger("twinseal").error(f"Cleanup error: {e}")
        await asyncio.sleep(interval_seconds)
