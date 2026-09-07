import asyncio
import sys
from pathlib import Path

import os
import logging
from arq.connections import RedisSettings

# ตั้งค่า Logging แบบง่ายสำหรับ Worker โดยเฉพาะ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | worker | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("worker_service")



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


import mlflow.pyfunc

# Cache for loaded models
model_cache = {}

async def inference_task(ctx, model_uri: str, input_data: list) -> dict:
    """Inference task that loads a model from MLflow and makes predictions."""
    logger.info(f"Starting inference using model: {model_uri}")
    
    # Check if model is already loaded in cache
    if model_uri not in model_cache:
        logger.info("Model not in cache, loading from MLflow...")
        try:
            # Set MLflow tracking URI just in case
            import os
            mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
            # For CPU/Async context, it's safe to load here or use a thread pool.
            # We'll load directly.
            model = mlflow.pyfunc.load_model(model_uri)
            model_cache[model_uri] = model
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return {"status": "error", "error": str(e)}
    
    model = model_cache[model_uri]
    
    try:
        # Predict
        predictions = model.predict(input_data)
        
        # Convert predictions to a format that can be serialized
        if hasattr(predictions, "tolist"):
            predictions = predictions.tolist()
            
        return {
            "status": "success",
            "model_uri": model_uri,
            "predictions": predictions
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return {"status": "error", "error": str(e)}


from training_worker import train_model

class WorkerSettings:
    functions = [process_data_task, minio_file_processor_task, train_model, inference_task]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://redis:6379"))
    max_jobs = 10
    poll_delay = 0.5


if __name__ == "__main__":
    print("Run worker using: arq workers.worker.WorkerSettings")
