import logging
import os
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime


class CustomLogger:
    """
    Custom Logger ที่รองรับหลักการพื้นฐานของการทำ Log
    
    หลักการออกแบบ:
    1. Singleton Pattern - มี Instance เดียวตลอดการทำงานของระบบ
    2. Multiple Handlers - รองรับทั้ง Console และ File
    3. Log Rotation - ป้องกันไฟล์ใหญ่เกินไป
    4. Structured Format - รูปแบบชัดเจน อ่านง่าย
    5. Configurable Levels - ตั้งค่าระดับ Log ได้ตาม Environment
    """
    
    _instance = None
    _logger = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton Pattern: สร้าง Instance เดียวเท่านั้น"""
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
        return cls._instance
    
    def __init__(
        self, 
        name="ProjectLogger", 
        log_dir="logs",
        log_level=logging.DEBUG,
        max_bytes=5*1024*1024,  # 5MB
        backup_count=3
    ):
        """
        Initialize Logger
        
        Args:
            name: ชื่อ Logger
            log_dir: โฟลเดอร์เก็บไฟล์ Log
            log_level: ระดับ Log ต่ำสุดที่จะบันทึก
            max_bytes: ขนาดไฟล์สูงสุดก่อนหมุนเวียน
            backup_count: จำนวนไฟล์สำรองที่เก็บไว้
        """
        # ป้องกันการ Initialize ซ้ำ
        if self._logger is not None:
            return
        
        # สร้าง Logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(log_level)
        
        # ป้องกันการเพิ่ม Handler ซ้ำ (กรณี Singleton ถูกเรียกหลายครั้ง)
        if self._logger.handlers:
            return
        
        # สร้างโฟลเดอร์ logs ถ้ายังไม่มี
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # กำหนดรูปแบบ Log (Format)
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # === Handler 1: Console Handler (แสดงบนหน้าจอ) ===
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)  # แสดงเฉพาะ INFO ขึ้นไป
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # === Handler 2: File Handler (บันทึกลงไฟล์) ===
        # ใช้ RotatingFileHandler เพื่อหมุนเวียนไฟล์
        log_file = os.path.join(log_dir, f"{name.lower()}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,      # ตัดเมื่อไฟล์ถึง 5MB
            backupCount=backup_count,  # เก็บไฟล์เก่า 3 ไฟล์
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # บันทึกทุก Level
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        
        # === Handler 3: Error File Handler (แยกไฟล์ Error) ===
        # บันทึกเฉพาะ ERROR และ CRITICAL ลงไฟล์แยก
        error_log_file = os.path.join(log_dir, f"{name.lower()}_error.log")
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self._logger.addHandler(error_handler)
    
    def get_logger(self):
        """ดึง Logger Instance ไปใช้งาน"""
        return self._logger


# === ฟังก์ชัน Helper สำหรับใช้งานง่าย ===
def get_logger(name="ProjectLogger"):
    """
    ฟังก์ชันสำหรับดึง Logger ไปใช้งาน
    
    Usage:
        logger = get_logger("auth_service")
        logger.info("User logged in")
    """
    return CustomLogger(name=name).get_logger()


# === ตัวอย่างการใช้งาน ===
if __name__ == "__main__":
    # สร้าง Logger
    logger = get_logger("test_module")
    
    # ทดสอบ Log ทุกระดับ
    logger.debug("This is DEBUG - Information for debugging")
    logger.info("This is INFO - System is operating normally")
    logger.warning("This is WARNING - Proceed with caution")
    logger.error("This is ERROR - An error occurred")
    logger.critical("This is CRITICAL - A critical failure occurred")
    
    print("\nLogger created successfully! Check the files in the logs/ directory.")