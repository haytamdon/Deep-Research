from concurrent.futures import ThreadPoolExecutor
from utils.pydantic_models import SubQueriesSearchMetadata, QuerySearchMetadata
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

def parallel_run_metadata(function, num_max_workers, params, client, model_name):
    with ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        futures = [executor.submit(function, param, client, model_name) for param in params]
        results = [f.result() for f in futures]
    return results

def parallel_run_search(function, num_max_workers, params, client, search_mode, output_type):
    # with ThreadPoolExecutor(max_workers=num_max_workers) as executor:
    #     futures = [executor.submit(function, client, query, search_mode, output_type, None, from_date, to_date) for query, from_date, to_date in params]
    #     results = [f.result() for f in futures]
    results = []
    for query, from_date, to_date in params:
        logger.info(f"Searching: {query} ...")
        results.append(function(client, query, search_mode, output_type, None, from_date, to_date))
    return results


def format_all_questions_output(parallel_output: List[QuerySearchMetadata]) -> SubQueriesSearchMetadata:
    main_query = parallel_output[0]
    sub_queries = parallel_output[1:]
    all_metadata_objects = SubQueriesSearchMetadata(
        main_query= main_query,
        sub_query_meta= sub_queries)
    return all_metadata_objects