from fastapi import Request, HTTPException
import asyncio
from datetime import datetime
from api.predict.schema import InferenceRequest, InferenceResponse
from utils.logger import get_logger

logger = get_logger("predict_controller")

async def predict(request_data: InferenceRequest, request: Request) -> InferenceResponse:
    job_id = f"infer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 1. validate request is done by Pydantic schema InferenceRequest
    
    redis_pool = request.app.state.redis_pool
    
    try:
        # 2. enqueue inference job
        job = await redis_pool.enqueue_job(
            'inference_task',
            request_data.model_uri,
            request_data.input_data,
            _job_id=job_id,
            _queue_name="inference_queue"
        )
        
        if not job:
            raise HTTPException(status_code=500, detail="Failed to enqueue inference job")
            
        logger.info(f"Enqueued inference job {job_id}")
        
        # 3. handle job result (wait for worker to process)
        # ตั้ง timeout ที่สมเหตุสมผล เช่น 30 วินาที
        result = await job.result(timeout=30.0)
        
        if result.get("status") == "error":
            logger.error(f"Inference job {job_id} error from worker: {result.get('error')}")
            # 5. handle error
            raise HTTPException(status_code=500, detail=result.get("error"))
            
        # 4. return response
        return InferenceResponse(
            status=result.get("status", "success"),
            model_uri=result.get("model_uri", request_data.model_uri),
            predictions=result.get("predictions", []),
            job_id=job_id
        )
        
    except asyncio.TimeoutError:
        logger.error(f"Inference job {job_id} timed out waiting for worker")
        raise HTTPException(status_code=504, detail="Inference process timed out")
    except Exception as e:
        logger.error(f"Inference job {job_id} failed: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Inference process failed: {str(e)}")
