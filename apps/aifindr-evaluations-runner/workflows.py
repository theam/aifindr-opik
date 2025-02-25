import logging
import time
import json
import requests
from settings import settings
from sseclient import SSEClient
from pydantic import BaseModel
from typing import Optional, List, Any

MAX_RETRIES = 5
RETRIEVAL_EVENT_ID_PREFIX = "similarity_search_by_text"
LLM_EVENT_ID_PREFIX = "llm"

logger = logging.getLogger(__name__)

class WorkflowResponse(BaseModel):
    context: Optional[List[Any]] = None
    response: str = ""


def run_workflow(workflow: str, query: str) -> WorkflowResponse:
    """
    Executes a workflow with the given query and handles retries.
    
    Args:
        workflow: The workflow identifier/path
        query: The query to process
        
    Returns:
        WorkflowResponse: The processed response containing retrieval and LLM responses
    """
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            return _make_workflow_request(workflow, query)
        except Exception as e:
            wait_time = 0.5 * (retry_count + 1)  # Increasing delay between retries
            logger.warn(f"Request failed with error: {e}. Waiting {wait_time}s before retrying... ({retry_count + 1}/{MAX_RETRIES})")
            retry_count += 1
            time.sleep(wait_time)
            
    raise Exception(f"Failed to complete request after {MAX_RETRIES} retries") 


def _make_workflow_request(workflow: str, query: str) -> WorkflowResponse:
    """
    Makes a POST request to the Ellmental API and processes SSE responses.
    
    Args:
        workflow: The workflow identifier/path
        query: The query to process
        
    Returns:
        WorkflowResponse: A model containing the retrieval response and concatenated LLM responses
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    logger.info(f"Running workflow: {workflow} with query: {query}")
    response = requests.post(
        f"{settings.ELLMENTAL_API_URL}{workflow}",
        stream=True,
        headers={
            "Authorization": f"Bearer {settings.ELLMENTAL_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        },
        json={
            "query": query,
            "stream": "true"
        },
    )
    
    if not response.ok:
        raise requests.exceptions.RequestException(f"Error calling Ellmental API: {response.text}")
    
    client = SSEClient(response)
    retrieval_response = None
    llm_response = ''
    
    for event in client.events():
        if not event.data:
            continue
            
        try:
            data = json.loads(event.data)
            if event.id.startswith(RETRIEVAL_EVENT_ID_PREFIX):
                logger.debug(f"Retrieval response: {data}")
                retrieval_response = data['response']['hits']
            elif event.id.startswith(LLM_EVENT_ID_PREFIX) and 'content' in data['delta']['message']:
                llm_response += data['delta']['message']['content']
        except json.JSONDecodeError as e:
            print(f"Failed to parse event data: {event.data}. Error: {e}")
            
    return WorkflowResponse(
        context=retrieval_response,
        response=llm_response
    )