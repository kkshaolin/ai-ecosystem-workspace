import asyncio
import sys
from pathlib import Path

# เพิ่ม path ของ backend
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from arq import create_pool
from arq.connections import RedisSettings
from core.config import settings


async def main():
    # สร้าง Redis connection
    print("Connecting to Redis...")
    redis = await create_pool(
        RedisSettings(
            host="localhost",
            port=6379,
        )
    )
    
    # Enqueue jobs หลายแบบ
    print("\nEnqueuing jobs...")
    
    # Job 1: ส่ง args
    job1 = await redis.enqueue_job(
        "simple_work",
        "Hello",
        "World",
        _queue_name="arq:queue",
    )
    print(f"Job 1 enqueued: {job1.job_id}")
    
    # Job 2: ส่ง kwargs
    job2 = await redis.enqueue_job(
        "simple_work",
        name="John",
        age=30,
        _queue_name="arq:queue",
    )
    print(f"Job 2 enqueued: {job2.job_id}")
    
    # Job 3: ส่งทั้ง args และ kwargs
    job3 = await redis.enqueue_job(
        "simple_work",
        "Task A",
        priority="high",
        _queue_name="arq:queue",
    )
    print(f"Job 3 enqueued: {job3.job_id}")
    
    print("\nWaiting for worker to process...")
    await asyncio.sleep(3)
    
    # เช็คว่า job เสร็จหรือยัง
    print("\nChecking job status...")
    for job in [job1, job2, job3]:
        status = await job.status()
        print(f"Job {job.job_id} status: {status}")
    
    await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())