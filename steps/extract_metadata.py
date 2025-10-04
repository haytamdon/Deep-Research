from datetime import date
from cerebras.cloud.sdk import Cerebras
from utils.prompts import METADATA_EXTRACTION_PROMPT
from utils.pydantic_models import QuerySearchMetadata
from utils.schemas import SearchDates
import logging
from utils.llm_utils import format_output_schema, call_cerebras_model
from typing import List
import json

logger = logging.getLogger(__name__)

def fallback_date_outputs(query):
    to_date = None
    from_date = None
    metadata_object = QuerySearchMetadata(query=query,
                                          from_date= from_date,
                                          to_date= to_date)
    return metadata_object

def extract_output_dict(response, query) -> QuerySearchMetadata:
    response_dict = json.loads(response.choices[0].message.content)
    to_date = response_dict['to_date']
    from_date = response_dict['from_date']
    metadata_object = QuerySearchMetadata(query=query,
                                          from_date= from_date,
                                          to_date= to_date)
    return metadata_object

def metadata_extraction_step(query: str, 
                             client: Cerebras,
                             model_name: str,
                             current_date: date = date.today()):
    
    logger.info(f"Decomposing research query: {query}")

    system_prompt = METADATA_EXTRACTION_PROMPT + f"\nFor more details here is the current date {current_date}."

    pydantic_schema = SearchDates.model_json_schema()

    output_schema = format_output_schema(pydantic_schema)

    try:
        output = call_cerebras_model(client, system_prompt, model_name, query, output_schema)
        query_metadata_obj = extract_output_dict(output)
    except:
        query_metadata_obj = fallback_date_outputs(query)

    return query_metadata_obj