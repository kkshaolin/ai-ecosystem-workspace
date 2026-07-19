from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # กำหนดตัวแปรและประเภทข้อมูล (Type Hinting)
    API_KEY: str
    APP_NAME: str = "Eco App"
    APP_ENV: str = "development"
    SECRET_KEY: SecretStr = "change-me"
    DEBUG: bool = False  # สามารถใส่ Default Value ได้
    PORT: int = 8080    # Pydantic จะแปลงชนิดข้อมูลจาก String ใน .env เป็น Int ให้เอง

    # ค่าเชื่อมต่อ Database (PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/mydb"
    
    # ค่าเชื่อมต่อ Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # ค่าเชื่อมต่อ Label Studio
    LABEL_STUDIO_API_KEY: str = ""
    LABEL_STUDIO_URL: str = "http://localhost:8080"

    # ตั้งค่าคอนฟิกเพื่อเชื่อมโยงกับไฟล์ .env
    model_config = SettingsConfigDict(
        env_file=".env",              # ระบุตำแหน่งไฟล์ .env
        env_file_encoding="utf-8",    # ระบุการถอดรหัสไฟล์
        extra="ignore"                # ถ้าใน .env มีตัวแปรอื่นที่ไม่ได้กำหนดไว้ในนี้ ให้ข้ามไป (ไม่ฟ้อง Error)
    )

# เรียกใช้งาน
settings = Settings()

# print(settings.DATABASE_URL)  # ผลลัพธ์: postgresql://user:pass@localhost:5432/db
# print(settings.PORT)          # ผลลัพธ์: 8000 (เป็นชนิดข้อมูล int เรียบร้อยแล้ว)
# print(type(settings.DEBUG))   # ผลลัพธ์: <class 'bool'> (แปลงจาก "true" ใน .env เป็น True)
