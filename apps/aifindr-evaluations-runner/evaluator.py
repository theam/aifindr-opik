import logging
from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (Hallucination, ContextRecall, ContextPrecision)
from workflows import run_workflow
from metrics.follows_criteria import FollowsCriteria
from pydantic import BaseModel
from enum import Enum

logger = logging.getLogger(__name__)

class ExperimentStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed" # Not used yet
    FAILED = "failed" # Not used yet


class EvaluationParams(BaseModel):
    task_id: str
    workspace_name: str
    dataset_name: str
    experiment_name: str
    project_name: str
    base_prompt_name: str
    workflow: str

def evaluation_task(dataset_item, workflow: str):
    # TODO: validate properly dataset_item so that no field is empty
    if not dataset_item['query']:
        logger.error("Trying to run workflow with an empty query")
        return {
            "input": "invalid-query",
            "output": "invalid-query",
            "context": [],
        }
    

    response_content = run_workflow(workflow, dataset_item['query'])

    # parsed_response = json.loads(response_content.response)
    # logger.info("------> Response: ", parsed_response)
    # logger.info("------> Response keys: ", parsed_response.keys())
    # logger.info("------> Response text_response: ", parsed_response['text_response'])

    result = {
        "input": dataset_item['query'],
        "output": response_content.response,
        "context": response_content.context,
    }
    return result

def build_evaluation_task(params: EvaluationParams):
    return lambda dataset_item: evaluation_task(dataset_item, params.workflow)


def execute_evaluation(params: EvaluationParams):
    client = Opik()
    dataset = client.get_dataset(name=params.dataset_name)
    base_prompt = client.get_prompt(name=params.base_prompt_name)
    if not base_prompt:
        raise ValueError(f"No base prompt found with name '{params.base_prompt_name}'")
    
    metrics = [FollowsCriteria(base_prompt.prompt), Hallucination(), ContextRecall(), ContextPrecision()]
    
    evaluate(
        experiment_name=params.experiment_name,
        dataset=dataset, 
        task=build_evaluation_task(params),
        scoring_metrics=metrics,
        project_name=params.project_name,
        experiment_config={
            "base_prompt_version": base_prompt.commit,
            "task_id": params.task_id
        },
        scoring_key_mapping={"expected_output": "criteria"}, # Used by Context* related metrics
        prompt=base_prompt,
        task_threads=20
    )
