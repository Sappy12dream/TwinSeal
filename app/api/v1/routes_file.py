# app/api/v1/routes_file.py
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.api.v1.dependencies import get_current_user
from app.core.encryption import encrypt_file, decrypt_file, save_encrypted_file, load_encrypted_file
from app.schemas.file import FileOut
from app.crud import file as crud_file
from app.crud import activity as crud_activity
from app.config import settings
import secrets

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Exception handler for rate limiting
@router.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# Upload file
@router.post("/upload", response_model=FileOut)
@limiter.limit("5/minute")  # Limit uploads per IP
async def upload_file(
    paired_user_id: int,
    file: UploadFile = Depends(),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Read file bytes
    file_bytes = await file.read()

    # Generate a random filename for storage
    stored_filename = secrets.token_hex(16)

    # Encrypt file using per-app key (can extend to per-user key)
    encrypted_bytes = encrypt_file(file_bytes, settings.secret_key.encode())

    # Save encrypted file
    save_encrypted_file(encrypted_bytes, stored_filename, settings.file_storage_path)

    # Store file metadata in DB
    db_file = await crud_file.create_file(
        db=db,
        filename=file.filename,
        stored_filename=stored_filename,
        owner_id=current_user.id,
        paired_user_id=paired_user_id
    )

    # Log upload activity
    await crud_activity.log_activity(
        db,
        current_user.id,
        "upload",
        f"File: {file.filename}, paired_user: {paired_user_id}"
    )
    return db_file

# Download file
@router.get("/download/{file_id}")
@limiter.limit("10/minute")  # Limit downloads per IP
async def download_file(
    file_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    db_file = await crud_file.get_file_by_id(db=db, file_id=file_id)
    if not db_file or (current_user.id not in [db_file.owner_id, db_file.paired_user_id]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Load encrypted bytes
    encrypted_bytes = load_encrypted_file(db_file.stored_filename, settings.file_storage_path)

    # Decrypt
    decrypted_bytes = decrypt_file(encrypted_bytes, settings.secret_key.encode())

    # Log download activity
    await crud_activity.log_activity(
        db,
        current_user.id,
        "download",
        f"File: {db_file.filename}, owner: {db_file.owner_id}"
    )

    return {
        "filename": db_file.filename,
        "file_bytes": decrypted_bytes
    }
