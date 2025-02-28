from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import asyncio
import uuid
from evaluator import EvaluationParams, ExperimentStatus, execute_evaluation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

TASK_QUEUE: asyncio.Queue[EvaluationParams] = asyncio.Queue(maxsize=10)  # Maximum number of evaluations in queue
MAX_CONCURRENT_TASKS = 5  # Number of concurrent evaluations

class RunEvaluationsRequest(BaseModel):
    workspace_name: str
    dataset_name: str
    experiment_name: str
    project_name: str | None = None
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
            # Run execute_evaluation in a thread pool so that it doesn't block the event loop
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, execute_evaluation, evaluation_params)
        except Exception as e:
            logger.error(f"Error processing evaluation: {str(e)}")
        finally:
            TASK_QUEUE.task_done()

@app.on_event("startup")
async def startup_event():
    # Start background workers to process the queue
    for _ in range(MAX_CONCURRENT_TASKS):
        asyncio.create_task(process_queue())

@app.post("/evaluations/run", response_model=RunEvaluationsResponse)
async def run_evaluation(input: RunEvaluationsRequest, req: Request):
    try:
        # Generate task ID
        task_id = str(uuid.uuid4())
        # Create EvaluationParams with all fields from request plus task_id
        evaluation_params = EvaluationParams(
            task_id=task_id,
            workspace_name=input.workspace_name,
            dataset_name=input.dataset_name,
            experiment_name=input.experiment_name,
            project_name=input.project_name,
            base_prompt_name=input.base_prompt_name,
            workflow=input.workflow,
            api_key=req.headers.get("Authorization")
        )

        try:
            TASK_QUEUE.put_nowait(evaluation_params)
            logger.info("Evaluation task added to queue")
        except asyncio.QueueFull:
            logger.error(f"Queue is full. Evaluation task not added to the queue: {evaluation_params}")
            raise HTTPException(status_code=503, detail="Server is currently at maximum capacity. Please try again later.")
        
        return RunEvaluationsResponse(status=ExperimentStatus.RUNNING.value, task_id=task_id)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
    