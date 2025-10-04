from fastapi import APIRouter
from dotenv import load_dotenv
from steps.query_decomposition import query_decomposition_step
from steps.extract_metadata import metadata_extraction_step
from steps.sub_question_search import parallelize_question_search
from utils.llm_utils import get_cerebras_client
from utils.search_utils import get_linkup_client
from utils.pydantic_models import SearchRequest, QuerySubQueryResults
from utils.utils import parallel_run_metadata, format_all_questions_output
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
    results = parallel_run_metadata(function= metadata_extraction_step, 
                                    num_max_workers= max_sub_questions, 
                                    params= questions, 
                                    client= cerebras_client, 
                                    model_name= model_name)
    formatted_result = format_all_questions_output(results)

    all_search_results = parallelize_question_search(all_questions=formatted_result,
                                client= linkup_client)
    return all_search_results