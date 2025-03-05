from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
import asyncio
import uuid
from requests import request, Response

from urllib.parse import urljoin, urlparse
from typing import Dict

from settings import settings
from evaluator import EvaluationParams, ExperimentStatus, execute_evaluation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

TASK_QUEUE: asyncio.Queue[EvaluationParams] = asyncio.Queue(
    maxsize=10
)  # Maximum number of evaluations in queue
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


class HealthResponse(BaseModel):
    ellmental: Dict[str, str]
    opik: Dict[str, str]


def get_domain(url: str) -> str:
    return urlparse(url).netloc.split(":")[0]


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


@app.get("/health", response_model=HealthResponse)
async def health(timeout: int = 5):
    ellmental_health_url: str = urljoin(settings.ELLMENTAL_API_URL, "/health")
    opik_health_url: str = urljoin(settings.OPIK_URL_OVERRIDE, "/is-alive/ping")

    ellm_health = {"status": "healthy", "message": "eLLMental is healthy"}
    opik_health = {"status": "healthy", "message": "OPIK is healthy"}
    try:
        ellm_response: Response = request(
            method="GET", url=ellmental_health_url, timeout=timeout
        )
        if ellm_response.status_code != 200:
            ellm_health["status"] = "unhealthy"
            ellm_health["message"] = str(ellm_response.text).replace(
                get_domain(settings.ELLMENTAL_API_URL), "***"
            )
    except Exception as e:
        ellm_health["status"] = "unhealthy"
        ellm_health["message"] = str(e).replace(
            get_domain(settings.ELLMENTAL_API_URL), "***"
        )
    try:
        opik_response: Response = request(
            method="GET", url=opik_health_url, timeout=timeout
        )
        if opik_response.status_code != 200:
            opik_health["status"] = "unhealthy"
            opik_health["message"] = str(opik_response.text).replace(
                get_domain(settings.OPIK_URL_OVERRIDE), "***"
            )
    except Exception as e:
        opik_health["status"] = "unhealthy"
        opik_health["message"] = str(e).replace(
            get_domain(settings.OPIK_URL_OVERRIDE), "***"
        )

    response = {"ellmental": ellm_health, "opik": opik_health}

    if all(health["status"] == "healthy" for health in [ellm_health, opik_health]):
        return HealthResponse(**response)
    else:
        raise HTTPException(status_code=503, detail=response)


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
            logger.error(
                f"Queue is full. Evaluation task not added to the queue: {evaluation_params}"
            )
            raise HTTPException(
                status_code=503,
                detail="Server is currently at maximum capacity. Please try again later.",
            )

        return RunEvaluationsResponse(
            status=ExperimentStatus.RUNNING.value, task_id=task_id
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
