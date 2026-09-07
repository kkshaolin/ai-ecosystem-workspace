from pydantic import BaseModel, Field
from typing import Any, List

class InferenceRequest(BaseModel):
    model_uri: str = Field(..., description="MLflow model URI (e.g. models:/my_model/1 or runs:/<run_id>/model)", example="runs:/abc123def456/model")
    input_data: List[Any] = Field(..., description="Data to run prediction on", example=[{"inputs": ["The quick brown fox jumps over the lazy dog."]}])

class InferenceResponse(BaseModel):
    status: str
    model_uri: str
    predictions: Any
    job_id: str
