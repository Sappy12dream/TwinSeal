# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.security import SecurityMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio

from app.config import settings
from app.api.v1 import routes_user, routes_file, routes_activity
from app.core.logger import setup_logging
from app.tasks.cleanup import start_cleanup_loop

# --- Logging ---
setup_logging()

# --- FastAPI App ---
app = FastAPI(
    title="TwinSeal",
    description="Secure file sharing platform with user pairing",
    version="0.1.0",
)

# --- CORS Middleware ---
origins = [
    "https://yourfrontend.com",
    "https://another-allowed-origin.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Security Headers ---
app.add_middleware(
    SecurityMiddleware,
    content_security_policy="default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self';",
    content_security_policy_report_only=False,
    strict_transport_security=True,
    frame_deny=True,
)

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

# Example: Apply limiter globally or per-route
# You can apply to sensitive routes like file upload/download
@app.get("/upload")
@limiter.limit("10/minute")  # max 10 requests per minute per IP
async def upload_file_placeholder():
    return {"msg": "Upload endpoint placeholder"}

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    # Start background cleanup task
    asyncio.create_task(start_cleanup_loop(interval_seconds=3600))  # every hour

# --- Include Routers ---
app.include_router(routes_user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(routes_file.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(routes_activity.router, prefix="/api/v1/activity", tags=["Activity"])

# --- Health Check ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}
