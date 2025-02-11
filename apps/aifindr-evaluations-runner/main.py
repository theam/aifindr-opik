from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import asyncio
import uuid
from evaluator import EvaluationParams, ExperimentStatus, execute_evaluation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

TASK_QUEUE: asyncio.Queue[EvaluationParams] = asyncio.Queue(maxsize=100)  # Maximum number of evaluations in queue
MAX_CONCURRENT_TASKS = 5  # Number of concurrent evaluations

class RunEvaluationsRequest(BaseModel):
    dataset_name: str
    experiment_name: str
    project_name: str
    base_prompt_name: str
    workflow: str

class RunEvaluationsResponse(BaseModel):
    status: str
    task_id: str

async def process_queue():
    """Background task to process queued evaluations"""
    while True:
        # Get a task from the queue
        evaluation_params = await TASK_QUEUE.get()
        try:
            logger.info(f"PROCESSING EVALUATION: {evaluation_params.task_id}")
            execute_evaluation(evaluation_params)
        except Exception as e:
            logger.error(f"Error processing evaluation: {str(e)}")
        finally:
            # Mark the task as done
            TASK_QUEUE.task_done()

@app.on_event("startup")
async def startup_event():
    # Start background workers to process the queue
    for _ in range(MAX_CONCURRENT_TASKS):
        asyncio.create_task(process_queue())

@app.post("/evaluations/run", response_model=RunEvaluationsResponse)
async def run_evaluation(request: RunEvaluationsRequest):
    try:
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Create EvaluationParams with all fields from request plus task_id
        evaluation_params = EvaluationParams(
            task_id=task_id,
            dataset_name=request.dataset_name,
            experiment_name=request.experiment_name,
            project_name=request.project_name,
            base_prompt_name=request.base_prompt_name,
            workflow=request.workflow
        )

        logger.info(f"Try adding evaluation task to queue: {evaluation_params}")
        try:
            TASK_QUEUE.put_nowait(evaluation_params)
            logger.info(f"Evaluation task added to queue: {evaluation_params}")
        except asyncio.QueueFull:
            logger.error("Queue is full. Cannot add more tasks.")
            raise HTTPException(status_code=503, detail="Server is currently at maximum capacity. Please try again later.")
        
        return RunEvaluationsResponse(status=ExperimentStatus.RUNNING.value, task_id=task_id)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
    
