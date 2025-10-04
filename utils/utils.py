from concurrent.futures import ThreadPoolExecutor
from utils.pydantic_models import SubQueriesSearchMetadata, QuerySearchMetadata
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

def parallel_run_metadata(function, num_max_workers, params, client, model_name):
    """Parallel run the metadata extraction function.

    Args:
        function: The function to be run.
        num_max_workers: The number of workers to be used.
        params: The parameters to be used.
        client: The client to be used.
        model_name: The model name to be used.
    """
    with ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        futures = [executor.submit(function, param, client, model_name) for param in params]
        results = [f.result() for f in futures]
    return results


def parallel_process_queries(function, num_max_workers, params, client, model_name):
    """Parallel process the queries processing function.

    Args:
        function: The function to be run.
        num_max_workers: The number of workers to be used.
        params: The parameters to be used.
        client: The client to be used.
        model_name: The model name to be used.
    """
    with ThreadPoolExecutor(max_workers=num_max_workers) as executor:
        futures = [executor.submit(function, param, client, model_name) for param in params]
        results = [f.result() for f in futures]
    return results


def sequential_run_search(function, params, client, search_mode, output_type):
    """Sequentially run the searching linkup api call.

    Args:
        function: Linkup API call function.
        num_max_workers: The number of workers to be used.
        params: The list of parameters to be used.
        client: linkup client.
        search_mode: The search mode to be used.
        output_type: The output type to be parsed.
    """
    results = []
    for query, from_date, to_date in params:
        logger.info(f"Searching: {query} ...")
        results.append(function(client, query, search_mode, output_type, None, from_date, to_date))
    return results


def format_all_questions_output(parallel_output: List[QuerySearchMetadata]) -> SubQueriesSearchMetadata:
    """Format the all questions output.

    Args:
        parallel_output: List[QuerySearchMetadata]: The parallel output.

    Returns:
        SubQueriesSearchMetadata: The formatted output.
    """
    main_query = parallel_output[0]
    sub_queries = parallel_output[1:]
    all_metadata_objects = SubQueriesSearchMetadata(
        main_query= main_query,
        sub_query_meta= sub_queries)
    return all_metadata_objects