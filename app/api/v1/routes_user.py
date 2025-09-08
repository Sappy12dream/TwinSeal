# app/api/v1/routes_user.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

from app.schemas.user import UserCreate, UserOut, UserLogin, Token
from app.crud import user as crud_user
from app.crud import activity as crud_activity
from app.db.session import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Exception handler for rate limiting
@router.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# Signup
@router.post("/signup", response_model=UserOut)
@limiter.limit("5/minute")  # Limit signups to 5 per minute per IP
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await crud_user.create_user(
            db=db,
            username=user_in.username,
            email=user_in.email,
            password=user_in.password
        )
        # Log signup activity
        await crud_activity.log_activity(db, user.id, "signup")
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Login
@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # Limit login attempts to prevent brute-force
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_user_by_email(db=db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Log login activity
    await crud_activity.log_activity(db, user.id, "login")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
