from pydantic import BaseModel, Field
from typing import List
from datetime import date

class SearchRequest(BaseModel):
    query: str
    max_sub_questions: int = 10

class QuerySubQuestions(BaseModel):
    """Immutable context containing the research query and its decomposition.

    This artifact is created once at the beginning of the pipeline and
    remains unchanged throughout execution.

    Attributes:
        main_question (str): main question.
        sub_questions (List[str]): All the questions extracted from the main question.
        justifications (List[str]): Links between the main query and the subquestions.
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

class QuerySearchMetadata(BaseModel):
    query: str = Field(
        ..., description="Query to be searched"
    )
    from_date: date = Field(
        default=None,
        description="Date from when the search should start"
    )
    to_date: date = Field(
        default=None,
        description="Date from when the search should end"
    )
