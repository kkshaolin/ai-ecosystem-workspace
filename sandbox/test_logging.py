import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.src.utils.logger import get_logger

# สร้าง Logger สำหรับแต่ละโมดูล
app_logger = get_logger("main_app")
db_logger = get_logger("database")

def connect_database():
    """ตัวอย่างการใช้งาน Logger ในฟังก์ชัน"""
    db_logger.info("กำลังเชื่อมต่อฐานข้อมูล...")
    
    try:
        # สมมติว่าเชื่อมต่อสำเร็จ
        db_logger.info("เชื่อมต่อฐานข้อมูลสำเร็จ")
        return True
    except Exception as e:
        db_logger.error(f"เชื่อมต่อฐานข้อมูลล้มเหลว: {str(e)}")
        return False

def process_user_login(username):
    """อีกตัวอย่างการใช้งาน"""
    app_logger.info(f"User '{username}' กำลังเข้าสู่ระบบ")
    
    # สมมติว่า login สำเร็จ
    app_logger.info(f"User '{username}' เข้าสู่ระบบสำเร็จ")
    
    # ตัวอย่าง Warning
    if username == "admin":
        app_logger.warning("Admin login detected - ตรวจสอบความปลอดภัย")

if __name__ == "__main__":
    app_logger.info("=== แอปพลิเคชันเริ่มต้น ===")
    
    connect_database()
    process_user_login("admin")
    process_user_login("user123")
    
    app_logger.info("=== แอปพลิเคชันสิ้นสุด ===")