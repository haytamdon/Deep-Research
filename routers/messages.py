from fastapi import APIRouter
from dotenv import load_dotenv
from steps.query_decomposition import query_decomposition_step
from steps.extract_metadata import metadata_extraction_step
from steps.sub_question_search import parallelize_question_search
from steps.process_queries import process_queries_step, map_queries_to_enhanced_queries
from utils.llm_utils import get_cerebras_client
from utils.search_utils import get_linkup_client
from utils.pydantic_models import SearchRequest, QuerySubQueryResults
from utils.utils import parallel_run_metadata, format_all_questions_output, parallel_process_queries
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()
router = APIRouter()

cerebras_client = get_cerebras_client(os.environ.get("CEREBRAS_API_KEY"))

linkup_client = get_linkup_client(os.environ.get("LINKUP_API_KEY"))

@router.post("/", response_model= QuerySubQueryResults)
def search_pipeline(request: SearchRequest,
                    model_name: str = "llama-4-scout-17b-16e-instruct"):
    query = request.query
    max_sub_questions = request.max_sub_questions
    sub_queries = query_decomposition_step(main_query= query,
                                           model_name= model_name,
                                           num_sub_questions= max_sub_questions,
                                           client= cerebras_client)
    questions = [query] + sub_queries.sub_questions
    logger.info(f"Starting the metadata extraction for {len(questions)} questions")
    results = parallel_run_metadata(function= metadata_extraction_step, 
                                    num_max_workers= max_sub_questions, 
                                    params= questions, 
                                    client= cerebras_client, 
                                    model_name= model_name)
    logger.info("Formatting the results for the main query and the sub queries")
    formatted_result = format_all_questions_output(results)
    logger.info("Starting the queries processing for the main query and the sub queries")
    enhanced_search_queries = parallel_process_queries(function= process_queries_step, 
                                    num_max_workers= max_sub_questions, 
                                    params= questions, 
                                    client= cerebras_client, 
                                    model_name= model_name)
    search_queries_with_metadata = map_queries_to_enhanced_queries(formatted_result, enhanced_search_queries)
    logger.info("Starting the question search for the main query and the sub queries")
    all_search_results = parallelize_question_search(all_questions=search_queries_with_metadata,
                                client= linkup_client)
    logger.info("Returning the results")
    return all_search_results
    # return search_queries_with_metadata