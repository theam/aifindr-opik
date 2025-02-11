from opik.evaluation.metrics import base_metric, score_result
from opik.evaluation import models
from pydantic import BaseModel
import json
from typing import Any

class FollowsCriteriaResult(BaseModel):
    score: int
    reason: str

class FollowsCriteria(base_metric.BaseMetric):
    """
    A metric that evaluates whether an LLM's output follows specified criteria based on a prompt template.

    This metric uses another LLM to judge if the output adheres to the criteria defined in the prompt template.
    It returns a score between 0 and 1, where 1 indicates full compliance with the criteria.

    Args:
        prompt_template: The template string containing the base prompt where the specific item criteria will be inserted. It must contain the varaible "{criteria}" and "{output}" somewhere
        name: The name of the metric. Defaults to "Follows criteria"
        model_name: The name of the LLM model to use for evaluation. Defaults to "gpt-4"

    Example:
        >>> from metrics import FollowsCriteria
        >>> prompt_template = "You should follow the criteria listed here: {criteria}. The response to evaluate is: {output}" 
        >>> # Assuming criteria is "The response should be a country"
        >>> metric = FollowsCriteria(prompt_template=prompt_template)
        >>> result = metric.score('Spain')
        >>> print(result.value)
        1.0
        >>> print(result.reason)
        The output perfectly follows the criteria by providing the name of the country Spain
    """
    def __init__(self, prompt_template: str, name: str = "Follows criteria", model_name: str = "gpt-4o"):
        self.name = name
        self.llm_client = models.LiteLLMChatModel(model_name=model_name)
        self.prompt_template = f"""
{prompt_template}
-----
Answer with a json with the following format:
{{{{
    "score": <score float number between 0 and 1. 0 means the output does not follow the criteria at all, 1 means it follows the criteria perfectly. Any number between 0 and 1 means it follows the criteria to some extent: the closest to 1, the more it follows it.>,
    "reason": "<reason for the score>"
}}}}

        """.lstrip().rstrip()

    def score(self, output: str, criteria: str, **ignored_kwargs: Any):
        # Construct the prompt based on the output of the LLM
        prompt = self.prompt_template.format(
            output=output,
            criteria=criteria
        )

        print("Prompt total: ", prompt)
        # Generate and parse the response from the LLM
        response = self.llm_client.generate_string(input=prompt, response_format=FollowsCriteriaResult)

        response_dict = json.loads(response)
        return score_result.ScoreResult(
            name=self.name,
            value=response_dict["score"],
            reason=response_dict["reason"]
        )
    
    def ascore(self, output: str, criteria: str, **ignored_kwargs: Any):
        # TODO: Por ahora no funciona
        print("SCORE ASYNC")
        # await self._model.agenerate_string
        return self.score(output, criteria)