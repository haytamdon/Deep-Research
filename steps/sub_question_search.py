from utils.pydantic_models import SubQueriesSearchMetadata, QuerySubQueryResults
from utils.utils import parallel_run_search
from utils.search_utils import search_linkup, format_outputs
from typing import Literal
from linkup import LinkupClient
import logging

logger = logging.getLogger(__name__)

def parallelize_question_search(all_questions: SubQueriesSearchMetadata,
                                client: LinkupClient,
                                search_mode: Literal["standard", "deep"] = "standard",
                                output_type: Literal["searchResults", "sourcedAnswer", "structured"] = "sourcedAnswer"
                                ) -> QuerySubQueryResults:
    main_question = all_questions.main_query
    sub_questions = all_questions.sub_query_meta
    all_params = [(main_question.query, 
                   main_question.from_date, 
                   main_question.to_date)] + [(sub_question.query, 
                                               sub_question.from_date, 
                                               sub_question.to_date) for sub_question in sub_questions]
    num_max_workers = len(all_params)
    logger.info(f"Starting the question search for {num_max_workers} questions")
    outputs = parallel_run_search(function=search_linkup, 
                        num_max_workers= num_max_workers, 
                        params = all_params, 
                        client= client, 
                        search_mode= search_mode, 
                        output_type= output_type)
    all_questions = [main_question.query] + [sub_question.query for sub_question in sub_questions]
    formatted_search_results = format_outputs(queries= all_questions, search_results= outputs)
    return formatted_search_results