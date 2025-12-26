from langchain_core.tools import tool
from config.utils import get_top_cases
from gen_ai.call_llm import invoke_model
from gen_ai.prompts import get_summarise_profile_prompt


@tool
def get_user_profile(job_description: str, resume: str, user_id: str):
    """
    Use this tool to get the User Profile from Job Description, Resume & user_id.
    This tool takes in this 3 things and will return the User Profile.
    """
    print("in get user profile tool------")

    jd_summary = job_description[:1000]
    res_summary = resume[:1000]

    top_cases_list = get_top_cases(jd_summary = jd_summary, res_summary = res_summary, user_id = user_id)

    summarise_prompt = get_summarise_profile_prompt(top_cases_list = top_cases_list)

    response = invoke_model(prompt = summarise_prompt)

    return response