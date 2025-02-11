import json
from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (IsJson, Hallucination, AnswerRelevance, ContextRecall, ContextPrecision)
from pydantic import BaseModel
from workflows import run_workflow
from metrics.follows_criteria import FollowsCriteria

client = Opik()

class EvaluationParams(BaseModel):
    dataset_name: str
    experiment_name: str
    project_name: str
    base_prompt_name: str
    workflow: str


def evaluation_task(dataset_item, workflow: str):
    response_content = run_workflow(workflow, dataset_item['query'])

    # parsed_response = json.loads(response_content.response)
    # print(parsed_response)
    # print(parsed_response.keys())
    # print(parsed_response['text_response'])

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
    print("Base prompt: ", base_prompt.prompt)
    if not base_prompt:
        raise ValueError(f"No base prompt found with name '{params.base_prompt_name}'")
    # metrics = [IsJson(), AnswerRelevance(), Hallucination(), ContextRecall(), ContextPrecision(), FollowsCriteria(base_prompt.prompt)]
    metrics = [Hallucination(), FollowsCriteria(base_prompt.prompt)]
    
    eval_results = evaluate(
        experiment_name=params.experiment_name,
        dataset=dataset, 
        task=build_evaluation_task(params),
        scoring_metrics=metrics,
        project_name=params.project_name,
        experiment_config={
            "base_prompt_version": base_prompt.commit,
        },
        scoring_key_mapping={"expected_output": "criteria"}, # Used by Context* related metrics
        prompt=base_prompt,
        task_threads=20,
    )
    
    return eval_results
