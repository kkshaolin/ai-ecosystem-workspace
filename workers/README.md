#  Workers Service (Background Task Processing)

โฟลเดอร์นี้สำหรับเก็บบริการ **Background Worker** ที่ประมวลผลงานหนักแบบ Asynchronous โดยใช้ **ARQ** ร่วมกับ **Redis Broker**

- แยกงานที่ใช้เวลาคำนวณสูง (Heavy Workload) หรือประมวลผล AI/ML ออกจาก HTTP Web Request
- รับงานจาก Backend API ผ่าน Redis Task Queue เพื่อประมวลผลตามลำดับคิว
- รองรับงานเช่น: การดึงคุณลักษณะรูปภาพ (Feature Extraction), การประมวลผลไฟล์ Dataset จาก MinIO, การเทรนหรือรัน Inference โมเดล AI

##  รายการงานที่รองรับในปัจจุบัน (Tasks)
1. `process_data_task(ctx, task_id, payload)`:
   - งานประมวลผลข้อมูลทั่วไปในคิว
2. `minio_file_processor_task(ctx, object_name)`:
   - งานดึงและอ่านไฟล์ที่อัปโหลดเข้า MinIO เพื่อเตรียมนำไปทำ Indexing หรือประมวลผลโมเดล AI

##  ขั้นตอนการเพิ่มงาน AI Task ใหม่
1. เขียนฟังก์ชัน `async def my_ai_task(ctx, ...)` ใน `workers/worker.py`
2. ลงทะเบียนฟังก์ชันใน `WorkerSettings.functions = [..., my_ai_task]`
3. เรียกสั่งงานจาก Backend ด้วย `await redis.enqueue_job("my_ai_task", arg1, arg2)`
