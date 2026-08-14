import asyncio
import sys
from pathlib import Path

# Add backend directory to Python path for imports
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from arq.connections import RedisSettings  # noqa: E402
from core.config import settings  # noqa: E402
from utils.logger import get_logger  # noqa: E402

logger = get_logger("worker_service")


async def startup(ctx):
    logger.info("ARQ Worker starting up...")
    ctx["start_time"] = asyncio.get_event_loop().time()


async def shutdown(ctx):
    logger.info("ARQ Worker shutting down...")


async def process_data_task(ctx, task_id: str, payload: dict) -> dict:
    """Example background data processing task."""
    logger.info(f"[Task {task_id}] Started processing payload: {payload}")
    await asyncio.sleep(2)  # Simulate CPU/IO heavy work
    logger.info(f"[Task {task_id}] Processing complete.")
    return {"task_id": task_id, "status": "completed", "result": f"Processed {len(payload)} items"}


async def minio_file_processor_task(ctx, object_name: str) -> dict:
    """Task to process or extract features from files uploaded to MinIO."""
    logger.info(f"[MinIO Task] Processing object: {object_name}")
    await asyncio.sleep(1)
    return {"object_name": object_name, "status": "indexed"}


class WorkerSettings:
    functions = [process_data_task, minio_file_processor_task]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    max_jobs = 10
    poll_delay = 0.5


if __name__ == "__main__":
    print("Run worker using: arq workers.worker.WorkerSettings")
