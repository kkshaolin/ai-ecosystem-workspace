# Backend Service (FastAPI)

โฟลเดอร์นี้เก็บบริการ **Backend API** ของระบบ AI Ecosystem พัฒนาด้วย **FastAPI** ร่วมกับ **Async SQLAlchemy 2.0**, **PostgreSQL**, **Alembic**, **JWT Authentication** และการเชื่อมต่อกับ **MinIO** สำหรับเก็บไฟล์

- ให้บริการ RESTful API สำหรับระบบการลงทะเบียน เข้าสู่ระบบ และจัดการสิทธิ์ผู้ใช้งาน (Auth & Users)
- บริการ API อัปโหลดไฟล์ Dataset และข้อมูลสื่อเข้า MinIO Object Storage (`/api/storage`)
- เชื่อมต่อและส่งงานเข้า Background Task Queue (Redis + ARQ Worker)
- ตรวจสอบสถานะความพร้อมของโครงสร้างระบบด้วยระบบ Health Check แบบครบวงจร (`/health`)


## โครงสร้างภายในโฟลเดอร์ Backend

```text
backend/backend/
├── alembic/                  # ระบบจัดการ Database Schema Migration (Alembic)
│   ├── env.py                # ไฟล์ตั้งค่าการเชื่อมต่อ Async SQLAlchemy ของ Alembic
│   ├── script.py.mako        # Migration Script Template
│   └── versions/             # ไฟล์ประวัติบันทึกการเปลี่ยนแปลงตารางใน PostgreSQL
│       └── 548341a904e8_create_initial_tables.py
│
├── src/                      # Source Code หลักของ Backend
│   ├── main.py               # จุดเริ่มต้นแอป FastAPI, CORS Middleware และ Health Check
│   │
│   ├── api/                  # Controllers, Routers และ Data Schemas
│   │   ├── auth/             # ระบบลงทะเบียน, Login (JWT) (/api/auth)
│   │   │   ├── controller.py
│   │   │   ├── model.py
│   │   │   ├── repository.py
│   │   │   ├── router.py
│   │   │   ├── schema.py
│   │   │   └── service.py
│   │   ├── users/            # ระบบจัดการผู้ใช้งานแบบ CRUD (/api/users)
│   │   │   ├── controller.py
│   │   │   ├── router.py
│   │   │   └── schema.py
│   │   ├── storage/          # ระบบอัปโหลดไฟล์เข้า MinIO (/api/storage)
│   │   │   └── router.py
│   │   └── training/         # ระบบสั่งเทรนโมเดลและจัดการคิว (/api/training)
│   │       ├── controller.py
│   │       ├── schema.py
│   │       └── service.py
│   │
│   ├── core/                 # ไฟล์ตั้งค่าและคอนฟิกระบบ
│   │   ├── config.py         # อ่านค่าตัวแปรสภาพแวดล้อมจากไฟล์ .env ด้วย Pydantic Settings
│   │   └── worker_settings.py # ค่าคอนฟิกสำหรับ ARQ Redis Worker
│   │
│   ├── db/                   # การเชื่อมต่อฐานข้อมูล
│   │   └── database.py       # การสร้าง Async Engine, SessionLocal และ Base Classes
│   │
│   ├── models/               # SQLAlchemy Database Models
│   │   └── student.py        # Student Table Model
│   │
│   ├── services/             # Business Logic & Service Helpers
│   │   └── storage.py        # MinIO Storage Service สำหรับอัปโหลด/ดาวน์โหลดไฟล์
│   │
│   └── utils/                # ฟังก์ชันช่วยเหลือ
│       └── logger.py         # Custom Singleton Logger (Console & Rotating File Logs)
│
├── tests/                    # Unit Tests & Integration Tests
│   └── README.md
│
├── alembic.ini               # ไฟล์ตั้งค่าคำสั่ง Alembic
├── pyproject.toml            # Python Dependencies & Project Metadata (uv)
├── .env                      # ไฟล์เก็บตัวแปรสภาพแวดล้อม (Environment Variables)
└── README.md                 # Backend Service Documentation
├── alembic/                  # ระบบจัดการ Database Schema Migration (Alembic)
│   ├── versions/             # ไฟล์ประวัติบันทึกการเปลี่ยนแปลงตารางใน Postgres
│   └── env.py                # ไฟล์ตั้งค่าการเชื่อมต่อ Async SQLAlchemy ของ Alembic
│
├── api/                      # Controllers, Routers และ Data Schemas
│   ├── auth/                 # ระบบลงทะเบียน, Login (JWT), และดึงโปรไฟล์ผู้ใช้ (/api/auth)
│   ├── users/                # ระบบจัดการผู้ใช้งานแบบ CRUD (/api/users)
│   ├── storage/              # ระบบอัปโหลดไฟล์เข้า MinIO และสั่งงาน Worker (/api/storage)
│   └── training/             # ระบบสั่งเทรนโมเดล (เพิ่มคิว ARQ) และตรวจสอบสถานะ (/api/training)
│
├── core/                     # ไฟล์ตั้งค่าและคอนฟิกระบบ
│   ├── config.py             # การอ่านค่าตัวแปรสภาพแวดล้อมจากไฟล์ .env
│   └── worker_settings.py    # ค่าคอนฟิกสำหรับ ARQ Redis Worker
│
├── db/                       # การเชื่อมต่อฐานข้อมูล
│   └── database.py           # การสร้าง Async Engine และ Session Context Manager
│
├── models/                   # SQLAlchemy Database Models (เช่น User, Student)
│
├── services/                 # Business Logic & Service Helpers
│   └── storage.py            # MinIO Storage Service สำหรับอัปโหลด/ดาวน์โหลดไฟล์
│
├── main.py                   # จุดเริ่มต้นแอป FastAPI, CORS Middleware และ Health Check
├── alembic.ini               # ไฟล์ตั้งค่าคำสั่ง Alembic
├── pyproject.toml            # รายการ Python Dependencies
└── .env                      # ไฟล์เก็บตัวแปรสภาพแวดล้อม (Environment Variables)
```

---

## วิธีการรัน Backend

ก่อนรัน Server ให้สั่งอัปเดตตารางฐานข้อมูลใน PostgreSQL และ เตรียมสภาพแวดล้อมและอัปเดต schema ของฐานข้อมูล:

```
# Alembic อัปเดตฐานข้อมูล
python.exe -m alembic upgrade head
```

### 1. การรัน FastAPI Server
รัน Server ให้เรียกด้วย Python จาก `.venv`:

```
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. การเข้าใช้งาน API Documentation
เปิดใน Web Browser:
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Format**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📌
1. **การรันคำสั่ง**: ให้รันจาก Workspace Root เสมอ เพื่อให้การ Import Module ภายใน Python ทำงานได้ถูกต้อง
2. **สภาพแวดล้อม (.env)**: อย่า Commit ไฟล์ `.env` หรือ `.venv/` ขึ้น Git Repository
