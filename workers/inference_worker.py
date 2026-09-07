"""
Inference Worker - รับผิดชอบเฉพาะการทำ Inference จาก Model ที่เทรนเสร็จแล้ว
"""
import os
import asyncio
import logging
import mlflow.pyfunc
from arq.connections import RedisSettings

# ตั้งค่า Logging สำหรับ Inference Worker โดยเฉพาะ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | inference_worker | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("inference_worker")

# Cache สำหรับเก็บโมเดลที่โหลดแล้ว
model_cache = {}

# ตั้งค่า MLflow tracking URI เป็นตัวแปร Global
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

async def startup(ctx):
    """ฟังก์ชันทำงานเมื่อ Worker เริ่มต้น"""
    logger.info("Inference Worker starting up...")
    ctx["start_time"] = asyncio.get_event_loop().time()

async def shutdown(ctx):
    """ฟังก์ชันทำงานเมื่อ Worker ปิดตัว"""
    logger.info("Inference Worker shutting down...")
    model_cache.clear()
    logger.info("Cleared model cache.")

async def inference_task(ctx, model_uri: str, input_data: list) -> dict:
    """Inference task that loads a model from MLflow and makes predictions."""
    logger.info(f"Prediction started for model: {model_uri}")
    
    # ตรวจสอบว่าโมเดลอยู่ใน Cache หรือไม่
    if model_uri not in model_cache:
        logger.info(f"Model not in cache, Model loading from MLflow: {model_uri}")
        try:
            # โหลดโมเดล
            model = mlflow.pyfunc.load_model(model_uri)
            model_cache[model_uri] = model
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}", exc_info=True)
            return {"status": "error", "error": f"Model load failed: {str(e)}"}
    else:
        logger.info(f"Using cached model for {model_uri}")
        model = model_cache[model_uri]
    
    # ทำการพยากรณ์ (Prediction)
    try:
        logger.info("Prediction running...")
        predictions = model.predict(input_data)
        
        # จัดรูปแบบผลลัพธ์ให้สามารถ Serialize เป็น JSON ได้
        if hasattr(predictions, "tolist"):
            predictions = predictions.tolist()
            
        logger.info("Prediction completed successfully.")
        return {
            "status": "success",
            "model_uri": model_uri,
            "predictions": predictions
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return {"status": "error", "error": str(e)}

class WorkerSettings:
    """การตั้งค่าสำหรับ Inference Worker โดยเฉพาะ"""
    # ลงทะเบียนฟังก์ชันเฉพาะ inference ห้ามมี train_model
    functions = [inference_task]
    
    # ระบุ queue_name เป็น inference_queue
    queue_name = "inference_queue"
    
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(os.getenv("REDIS_URL", "redis://redis:6379"))
    max_jobs = 10
    poll_delay = 0.5

if __name__ == "__main__":
    print("Run inference worker using: arq workers.inference_worker.WorkerSettings")
