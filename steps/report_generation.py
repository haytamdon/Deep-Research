from typing import List, Dict

def formulate_main_query_subprompt_prompt(main_question: str,
                                      search_result: str,
                                      analysis: str) -> str:
    prompt = f"""The general question and topic of discussion is the following {main_question}.
    Here is the internet search result for that question {search_result}
    Here is the analysis 
    """
    return prompt