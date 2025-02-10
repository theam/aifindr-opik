from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
import logging
from evaluator import EvaluationParams, execute_evaluation

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class EvaluationResponse(BaseModel):
    result: Any

@app.post("/evaluations/run", response_model=EvaluationResponse)
async def run_evaluation(request: EvaluationParams):
    try:
        logger.debug(f"Received request: {request}")
        
        result = execute_evaluation(request)
        return EvaluationResponse(result=result)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
    
