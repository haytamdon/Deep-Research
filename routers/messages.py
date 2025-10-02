from fastapi import APIRouter
from dotenv import load_dotenv
from steps.query_decomposition import query_decomposition_step
from utils.llm_utils import get_cerebras_client
from utils.pydantic_models import QuerySubQuestions, SearchRequest
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()
router = APIRouter()

cerebras_client = get_cerebras_client(os.environ.get("CEREBRAS_API_KEY"))

@router.post("/", response_model=QuerySubQuestions)
def search_pipeline(request: SearchRequest):
    logger.info("test")
    query = request.query
    max_sub_questions = request.max_sub_questions
    sub_queries = query_decomposition_step(main_query= query,
                                           model_name="llama-4-scout-17b-16e-instruct",
                                           num_sub_questions= max_sub_questions,
                                           client= cerebras_client)
    return sub_queries