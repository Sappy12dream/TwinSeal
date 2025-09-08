# app/crud/pairing.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import secrets
from app.models.pairing import PairingID
from app.config import settings

async def create_pairing_id(db: AsyncSession, user_id: int) -> PairingID:
    code = secrets.token_urlsafe(16)
    expires_at = datetime.utcnow() + timedelta(hours=settings.temp_id_expire_hours)
    pairing = PairingID(user_id=user_id, code=code, expires_at=expires_at)
    db.add(pairing)
    await db.commit()
    await db.refresh(pairing)
    return pairing

async def get_pairing_id(db: AsyncSession, code: str) -> PairingID | None:
    result = await db.execute(
        select(PairingID).where(PairingID.code == code, PairingID.expires_at > datetime.utcnow())
    )
    return result.scalars().first()

async def delete_expired_pairing_ids(db: AsyncSession):
    result = await db.execute(
        select(PairingID).where(PairingID.expires_at <= datetime.utcnow())
    )
    expired = result.scalars().all()
    for item in expired:
        await db.delete(item)
    await db.commit()
