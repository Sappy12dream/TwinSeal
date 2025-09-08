# app/crud/file.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.file import File
from typing import List

async def create_file(
    db: AsyncSession,
    filename: str,
    stored_filename: str,
    owner_id: int,
    paired_user_id: int
) -> File:
    new_file = File(
        filename=filename,
        stored_filename=stored_filename,
        owner_id=owner_id,
        paired_user_id=paired_user_id
    )
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file

async def get_files_for_user(db: AsyncSession, user_id: int) -> List[File]:
    result = await db.execute(
        select(File).where((File.owner_id == user_id) | (File.paired_user_id == user_id))
    )
    return result.scalars().all()

async def get_file_by_id(db: AsyncSession, file_id: int):
    result = await db.execute(select(File).where(File.id == file_id))
    return result.scalars().first()
