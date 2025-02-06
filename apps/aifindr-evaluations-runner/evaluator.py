import os

from opik import Opik
from opik.evaluation import evaluate
from opik.evaluation.metrics import (Hallucination, Moderation, AnswerRelevance, ContextRecall, ContextPrecision)
from config import settings


os.environ["OPIK_URL_OVERRIDE"] = settings.OPIK_URL
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

client = Opik()
dataset = client.get_dataset(name="BCP eval dataset")
prompt = client.get_prompt(name="BCP eval prompt")

def evaluation_task(dataset_item):
    print("Experiment item: ", dataset_item)
    # your LLM application is called here



    result = {
        "input": dataset_item['query'],
        "output": "Es madrid",
        "context": []
    }
    return result


def execute_evaluation(dataset_name: str, experiment_name: str, project_name: str, base_prompt_name: str):
    client = Opik()
    dataset = client.get_dataset(name=dataset_name)
    base_prompt = client.get_prompt(name=base_prompt_name)
    metrics = [Hallucination(), Moderation(), AnswerRelevance(), ContextRecall(), ContextPrecision()]

    print("Base prompt: ", base_prompt)
    
    eval_results = evaluate(
        experiment_name=experiment_name,
        dataset=dataset, 
        task=evaluation_task,
        scoring_metrics=metrics,
        project_name=project_name,
        experiment_config={
            "pepe": "paco"
        },
        scoring_key_mapping={"expected_output": "criteria"},
        prompt=base_prompt
    )
    
    return eval_results
