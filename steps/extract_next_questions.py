from utils.pydantic_models import QueryReport, ReportNextSteps
from utils.prompts import NEXT_QUESTIONS_PROMPT
from utils.schemas import NextQuestionList, NextQuestion
from utils.llm_utils import format_output_schema, call_cerebras_model
import logging
from cerebras.cloud.sdk import Cerebras
from typing import List
import json

logger = logging.getLogger(__name__)

def extract_output_dict(response) -> List[NextQuestion]:
    response_dict = json.loads(response.choices[0].message.content)
    question_list = response_dict["questions"]
    return question_list

def next_query_creation(report_obj: QueryReport,
                        num_next_questions: int,
                        model_name: str,
                        client: Cerebras) -> ReportNextSteps:
    report = report_obj.report

    original_question = report_obj.main_query

    prompt_subfix = f"\nPlease generate {num_next_questions} questions to be explored."

    system_prompt = NEXT_QUESTIONS_PROMPT + prompt_subfix

    logger.info(f"Calling {model_name} to decompose query into {num_next_questions} sub-questions")

    pydantic_schema = NextQuestionList.model_json_schema()

    output_schema = format_output_schema(pydantic_schema)

    output = call_cerebras_model(client, system_prompt, model_name, report, output_schema)

    question_list = extract_output_dict(output)

    next_queries_obj = ReportNextSteps(main_query= original_question,
                                       report= report,
                                       next_questions= [question.question for question in question_list]
                                       )
    
    return next_queries_obj