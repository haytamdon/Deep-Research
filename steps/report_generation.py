from typing import List, Dict

def formulate_main_query_subprompt(main_question: str,
                                      search_result: str,
                                      analysis: str) -> str:
    sub_prompt = f"""The general question and topic of discussion is the following {main_question}.
    Here is the internet search result for that question {search_result}
    Here is the analysis of the query with search results {analysis}
    """
    return sub_prompt

def formulate_sub_query_subprompt(sub_question: str,
                                  search_result: str,
                                  analysis: str)-> str:
    sub_prompt = f"""A sub question generated out of the main question is the following {sub_question}.
    Here is the internet search result for that question {search_result}
    Here is the analysis of the query with search results {analysis}
    """
    return sub_prompt