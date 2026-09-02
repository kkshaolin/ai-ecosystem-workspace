#  AI Ecosystem Workspace

รีโพสิทอรีนี้เป็นโครงสร้างระบบ **AI Engineering Ecosystem** แบบครบวงจร พัฒนาขึ้นสำหรับการทำงานจริงในระดับต่อยอดรองรับระบบ AI (เช่น Computer Vision, LLM/RAG, หรือ Predictive Analytics) โดยแบ่งสัดส่วนการทำงานอย่างเป็นโมดูล (Modular Architecture) ใช้งานง่าย ปลอดภัย และพร้อมสำหรับการขยายระบบในอนาคต

##  โครงสร้างโฟลเดอร์และไฟล์สำคัญ (Directory Structure)

```text
ai-ecosystem-workspace/
├── backend/                  # บริการ Backend API (FastAPI)
│   │
│   ├── alembic/              # Database Migration Management (Alembic)
│   │
│   ├── src/                  # Source Code หลัก
│   │   │
│   │   ├── api/              # API Controllers, Routers & Schemas
│   │   │   ├── auth/         # ระบบยืนยันตัวตน (Authentication & JWT Tokens)
│   │   │   ├── users/        # ระบบจัดการผู้ใช้งาน (User Management CRUD)
│   │   │   ├── storage/      # ระบบอัปโหลดและจัดการไฟล์ Dataset บน MinIO
│   │   │   └── training/     # ระบบจัดการการเทรนโมเดล (Enqueue Job, Check Status)
│   │   │   
│   │   ├── core/             # ไฟล์ตั้งค่าส่วนกลาง (Configuration)
│   │   │
│   │   ├── db/               # การเชื่อมต่อฐานข้อมูล SQLAlchemy
│   │   │
│   │   ├── models/           # Data Models / Database Tables
│   │   │
│   │   ├── services/         # Helper Services & Business Logic
│   │   │
│   │   ├── utils/            # ฟังก์ชันช่วยเหลือ
│   │   │   └── logger.py     # Custom Singleton Logger (Console & Rotating File Logs)
│   │   │
│   │   └── main.py           # จุดเริ่มต้น FastAPI App, CORS, และ Health Check Endpoints
│   │
│   ├── tests/                # Unit Tests & Integration Tests
│   │
│   ├── alembic.ini           # Alembic Configuration File
│   ├── pyproject.toml        # Python Dependencies & Project Metadata
│   └── README.md             # Backend Service Documentation
│
├── diagrams/                 # ไดอะแกรมสถาปัตยกรรมและ Workflow
│
├── frontend/                 # พื้นที่สำหรับพัฒนาแอปพลิเคชันฝั่งหน้าเว็บ (Web UI Client)
│
├── sandbox/                  # สคริปต์สำหรับทดลองโค้ด (Proof of Concept Tests)
│
├── scripts/                  # สคริปต์ช่วยเหลือระบบ
│   ├── export_openapi_to_csv.py # Export OpenAPI Schema to CSV
│   ├── generate_label_studio_token.py # Generate Label Studio Auth Token
│   └── README.md
│
├── storage/                  # โฟลเดอร์เก็บข้อมูลจำลองและระบบ (Volume Data)
│   ├── data/                 # ที่เก็บข้อมูล Dataset & Label Studio
│   ├── logs/                 # ไฟล์ Log การทำงานของระบบ
│   ├── models/               # ที่เก็บไฟล์โมเดล AI
│   └── README.md
│
├── workers/                  # บริการ Worker ทำงานเบื้องหลัง (Background Worker)
│    ├── worker.py             # ARQ Worker Runner สำหรับประมวลผลงาน AI/ML ทั่วไป
│    ├── training_worker.py    # ARQ Worker สำหรับรันงานเทรนโมเดลด้วย PyTorch & GPU
│    └── README.md
│
├── compose.yml               # การตั้งค่า Docker Compose สำหรับคอนเทนเนอร์ทั้งหมด
└── README.md                 # ไฟล์ข้อมูลโครงการนี้

```



##  คุณสมบัติหลักที่ปรับปรุงให้พร้อมใช้งานจริง (Key Technical Features)

1. **FastAPI Architecture (Clean Layered Pattern)**:
   - แยกเลเยอร์ชัดเจน: `Router` -> `Controller` -> `Service` -> `Repository` -> `Database`
   - ปลอดภัยด้วย JWT Authentication และ Hashed Password (`pwdlib`)
2. **CORS Security Middleware**:
   - ตั้งค่าอนุญาตให้ Frontend (เช่น React, Vue, Next.js หรือ Vite) เรียกใช้งาน API ได้ผ่าน `CORS_ORIGINS`
3. **Database Migration ด้วย Alembic**:
   - ไม่ต้องเสี่ยงข้อมูลหายจากการใช้ `create_all()` ควบคุมเวอร์ชันของตารางใน PostgreSQL ด้วย Migration Scripts
4. **MinIO Object Storage Integration**:
   - บริการอัปโหลด/ดาวน์โหลดไฟล์ Dataset รองรับไฟล์ขนาดใหญ่ เข้า S3-compatible API
5. **ARQ Asynchronous Background Worker**:
   - สั่งงาน AI ที่คำนวณหนัก หรือประมวลผลรูปภาพเข้า Redis Queue เพื่อให้ Worker ทำงานเบื้องหลัง โดยไม่ทำให้ Web Server ค้าง
6. **Comprehensive Health Check Endpoint (`GET /health`)**:
   - ตรวจสอบสถานะความพร้อมของ PostgreSQL, Redis และ MinIO แบบเรียลไทม์
7. **Custom Rotating Logger**:
   - บันทึก Log ทั้งทาง Console และลงไฟล์แบบหมุนเวียน (Rotating File Logs) พร้อมแยกไฟล์ Error Log อัตโนมัติ



##  ขั้นตอนการติดตั้งและการรันระบบ (Getting Started Guide)

### ข้อกำหนดเบื้องต้น (Prerequisites)
- **Python**: เวอร์ชัน 3.11 ขึ้นไป
- **Docker & Docker Desktop**: สำหรับรันบริการฐานข้อมูลและ Storage

### 1. การสตาร์ทบริการด้วย Docker Compose

เปิด Terminal ใน Root Directory ของโปรเจกต์แล้วรันคำสั่ง:

```
docker compose up -d
```

### 2. การรัน FastAPI Backend Server

รัน Server ด้วย Uvicorn จาก Backend Directory:
```
cd backend
```

```
uv run python src/main.py
```



### 3. การรัน ARQ Background Worker

เปิด Terminal ใหม่เพื่อรันบริการ Worker ในการประมวลผลงานเบื้องหลังที่  Backend Directory:

```
uv run arq workers.worker.WorkerSettings
```


##  รายการ API Endpoints ที่สำคัญ (Key API Endpoints)

###  System Health Check
- `GET /health` : ตรวจสอบสถานะการเชื่อมต่อของระบบทั้งหมด (Postgres, Redis, MinIO)

###  Authentication & Users (`/api/auth`, `/api/users`)
- `POST /api/auth/register` : สมัครสมาชิกผู้ใช้งานใหม่
- `POST /api/auth/login` : เข้าสู่ระบบเพื่อรับ JWT Access Token
- `GET /api/auth/me` : ดูข้อมูลผู้ใช้ปัจจุบัน (ต้องส่ง Bearer Token)
- `GET /api/users` : เรียกดูรายชื่อผู้ใช้ทั้งหมดในระบบ

###  Storage & Dataset Management (`/api/storage`)
- `POST /api/storage/upload` : อัปโหลดไฟล์ Dataset เข้า MinIO และส่ง Job เข้า ARQ Worker
- `GET /api/storage/files` : ดึงรายการไฟล์ทั้งหมดใน MinIO ของผู้ใช้งานปัจจุบัน

###  Model Training (`/api/training`)
- `POST /api/training/add_train_queue_time` : สั่งเริ่มเทรนโมเดล (เพิ่ม Job เข้าคิว ARQ สำหรับ Training Worker)
- `GET /api/training/job_status/{job_id}` : ตรวจสอบสถานะการเทรนของโมเดล

---

## 📌 Notes

### Port Assignments (การกำหนด Port):
- **FastAPI Backend**: http://localhost:8000  Swagger UI: http://localhost:8000/docs
- **Label Studio**: http://localhost:8080
- **MinIO Web Console**: http://localhost:9001
- **PostgreSQL**: localhost:5433
- **Redis**: localhost:6379