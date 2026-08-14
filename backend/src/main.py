import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from core.config import settings
from db.database import create_database_schema, get_db_session
from api.auth.router import router as auth_router
from api.users.router import router as users_router
from api.storage.router import router as storage_router
from services.storage import storage_service
from utils.logger import get_logger

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
logger = get_logger("backend_main")


API_DESCRIPTION = """
🚀 **AI Ecosystem Backend Server APIs**

ระบบบริการสำหรับสถาปัตยกรรม **AI Engineering Ecosystem** แบบครบวงจร 

---

### 🧩 ส่วนประกอบและบริการของระบบ (System Components)
* 🔐 **Auth & User Services**: ระบบลงทะเบียน ยืนยันตัวตนผ่าน JWT Token และการจัดการผู้ใช้
* 📦 **Storage Services**: ระบบจัดการอัปโหลดไฟล์ Dataset และสื่อเข้า MinIO Object Storage
* ⚡ **Worker Task Services**: สั่งงานประมวลผลโมเดล AI / Data Ingestion เข้า Redis Queue (ARQ)
* 🩺 **Health Check Services**: ตรวจสอบสถานะการเชื่อมต่อบริการ PostgreSQL, Redis และ MinIO
"""

OPENAPI_TAGS = [
    {
        "name": "system",
        "description": "ระบบตรวจสอบสถานะความพร้อมและการเชื่อมต่อบริการรองรับทั้งหมด (Health Check & Diagnostics)",
    },
    {
        "name": "auth",
        "description": "ระบบการยืนยันตัวตน สมัครสมาชิก และออก JWT Access Token สำหรับเข้าใช้งาน",
    },
    {
        "name": "users",
        "description": "ระบบจัดการข้อมูลผู้ใช้งาน (User Management CRUD)",
    },
    {
        "name": "storage",
        "description": "ระบบอัปโหลดไฟล์ Dataset และภาพเข้า MinIO Object Storage พร้อมส่งงานเข้า Background Worker Queue",
    },
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in environment '{settings.APP_ENV}'...")
    try:
        await create_database_schema()
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.warning(f"Database schema initialization skipped or failed: {e}")
    
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=f"{settings.APP_NAME} - AI Ecosystem APIs",
    description=API_DESCRIPTION,
    version="1.0.0",
    terms_of_service="http://localhost:8000/terms",
    contact={
        "name": "AI Ecosystem Student Team",
        "url": "http://localhost:8000",
        "email": "student@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=OPENAPI_TAGS,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(storage_router, prefix="/api")


@app.get("/health", tags=["system"], summary="Comprehensive System Health Check")
async def health_check(session: AsyncSession = Depends(get_db_session)) -> dict:
    """Comprehensive health check endpoint checking Postgres, Redis, and MinIO services."""
    health_status = {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "services": {
            "database": "unknown",
            "redis": "unknown",
            "minio": "unknown",
        },
    }

    # 1. Check PostgreSQL
    try:
        await session.execute(text("SELECT 1"))
        health_status["services"]["database"] = "connected"
    except Exception as e:
        health_status["services"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # 2. Check Redis
    try:
        r = aioredis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        await r.ping()
        await r.aclose()
        health_status["services"]["redis"] = "connected"
    except Exception as e:
        health_status["services"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "degraded"

    # 3. Check MinIO
    if storage_service.is_healthy():
        health_status["services"]["minio"] = "connected"
    else:
        health_status["services"]["minio"] = "error: unreachable"
        health_status["status"] = "degraded"

    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)