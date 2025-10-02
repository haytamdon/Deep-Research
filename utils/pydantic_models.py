from pydantic import BaseModel, Field
from typing import List

class SearchRequest(BaseModel):
    query: str
    max_sub_questions: int = 10

class QuerySubQuestions(BaseModel):
    """Immutable context containing the research query and its decomposition.

    This artifact is created once at the beginning of the pipeline and
    remains unchanged throughout execution.
    """

    main_query: str = Field(
        ..., description="The main research question from the user"
    )
    sub_questions: List[str] = Field(
        default_factory=list,
        description="Decomposed sub-questions for parallel processing",
    )
    justifications: List[str] = Field(
        default_factory= list,
        description="Links between the main query and the subquestions"
    )