from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import logging
from evaluator import execute_evaluation

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class EvaluationRequest(BaseModel):
    dataset_name: str
    experiment_name: str
    project_name: str
    base_prompt_name: str
class EvaluationResponse(BaseModel):
    result: Dict[str, Any]

@app.post("/evaluations/run", response_model=EvaluationResponse)
async def run_evaluation(request: EvaluationRequest):
    try:
        logger.debug(f"Received request: {request}")
        
        result = execute_evaluation(request.dataset_name, request.experiment_name, request.project_name, request.base_prompt_name)
        return EvaluationResponse(result=result)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 