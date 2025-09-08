# app/api/v1/routes_pairing.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.crud import pairing as crud_pairing
from app.crud import activity as crud_activity
from app.db.session import get_db
from app.schemas.user import UserOut
from app.models.user import User
from app.api.v1.dependencies import get_current_user
from app.crud import user as crud_user

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Exception handler for rate limiting
@router.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# Generate a temporary pairing ID
@router.post("/generate", response_model=str)
@limiter.limit("5/minute")  # Limit to 5 per minute per IP
async def generate_pairing_id(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pairing = await crud_pairing.create_pairing_id(db=db, user_id=current_user.id)
    await crud_activity.log_activity(db, current_user.id, "generate_pairing_id", f"Code: {pairing.code}")
    return pairing.code

# Pair with another user using a code
@router.post("/pair/{code}", response_model=UserOut)
@limiter.limit("10/minute")  # Limit pairing attempts to 10 per minute per IP
async def pair_with_user(code: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    pairing = await crud_pairing.get_pairing_id(db=db, code=code)
    if not pairing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid or expired pairing code")
    
    # Return paired user info
    paired_user = await crud_user.get_user_by_id(db=db, user_id=pairing.user_id)
    await crud_activity.log_activity(db, current_user.id, "pair_account", f"Paired with user_id: {paired_user.id}")
    return paired_user
