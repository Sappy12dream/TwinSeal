# app/crud/activity.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity

async def log_activity(db: AsyncSession, user_id: int, action: str, details: str | None = None) -> Activity:
    activity = Activity(user_id=user_id, action=action, details=details)
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity

async def get_user_activities(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Activity).where(Activity.user_id == user_id).order_by(Activity.created_at.desc())
    )
    return result.scalars().all()
