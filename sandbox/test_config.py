import sys
from pathlib import Path

# เพิ่ม path ของ backend เข้าไป เพื่อให้ import core.config ได้
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.config import settings


def main():
    """ทดสอบการโหลดค่าจาก .env"""
    print("=" * 50)
    print("Testing Settings from .env file")
    print("=" * 50)
    
    print(f"App Name      : {settings.APP_NAME}")
    print(f"Environment   : {settings.APP_ENV}")
    print(f"Debug Mode    : {settings.DEBUG}")
    print(f"Database URL  : {settings.DATABASE_URL}")
    print(f"Redis URL     : {settings.REDIS_URL}")
    print(f"Label Studio : {settings.LABEL_STUDIO_URL}")
    print("=" * 50)
    
    # ตรวจสอบชนิดข้อมูล (Type checking)
    print("\nType Checking:")
    print(f"Type of DEBUG   : {type(settings.DEBUG).__name__}")
    print(f"Type of APP_NAME: {type(settings.APP_NAME).__name__}")


if __name__ == "__main__":
    main()