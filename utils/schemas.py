"""
Centralized collection of schemas used throughout the deep research pipeline.

This module contains all system schemas used by LLM calls in various steps of the
research pipeline to ensure consistency and make prompt management easier.
"""
from pydantic import BaseModel, Field
from typing import List

DEFAULT_SEARCH_QUERY_SCHEMA = {
  "type": "object",
  "properties": {
    "search_query": {"type": "string"},
    "reasoning": {"type": "string"}
  }
}

class SearchResult(BaseModel):
    search_query: str = Field(description="")
    reasoning: str = Field(description="")

class SubQuestion(BaseModel):
    sub_question: str = Field(description="A sub-question derived from the main question")
    reasoning: str = Field(description="The reasoning for why this sub-question is important")

class SubQuestionList(BaseModel):
    questions: List[SubQuestion] = Field(description="List of sub-questions")