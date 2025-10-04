"""
Collection of functions for calling LLMs and tools throughout the pipeline
"""
from cerebras.cloud.sdk import Cerebras
import os
from pydantic import SecretStr
from typing import Dict


def get_cerebras_client(api_key: SecretStr = SecretStr(os.environ.get("CEREBRAS_API_KEY"))):
    """Get the Cerebras client.

    Args:
        api_key (SecretStr): The API key for the Cerebras client.

    Returns:
        Cerebras: The Cerebras client.
    """
    client = Cerebras(
        api_key= api_key
    )
    return client

def call_cerebras_model(client, system_prompt, model_name, prompt, response_schema):
    """Call the Cerebras model.

    Args:
        client (Cerebras): The Cerebras client.
        system_prompt (str): The system prompt.
        model_name (str): The name of the model to be used.
        prompt (str): The prompt.
        response_schema (Dict[str, any]): The response schema.

    Returns:
        Completion: The completion of the model.
    """
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        response_format= response_schema
    )
    return completion

def format_output_schema(pydantic_json: Dict[str, any]):
    """Format the output schema.

    Args:
        pydantic_json (Dict[str, any]): The Pydantic JSON schema.

    Returns:
        Dict[str, any]: The formatted schema.
    """
    format_schema = {
                        "type": "json_schema", 
                        "json_schema": {
                            "name": "question_schema",
                            "strict": True,
                            "schema": pydantic_json
                        }
                    }
    return format_schema