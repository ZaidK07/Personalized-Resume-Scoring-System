system_prompt = """
- You are a personalized Resume Scoring Assstant.
- Your job is to take resume, job description & user profile(if available) into consideration and score
    particular resume against the required job description.

# ==========

Data Flow:

1. You will get Resume, Job Description & user_id.
2. Then use the tool which takes Job Description, Resume & user_id and returns the User's Profile.
3. After you have User's profile, Now you will have 4 things: (i) Job Description, (ii) Resume,
    (iii) User Profile / Preferences, (iv) user_id
4. Now your job is to evaluate Job Description, Resume & User's preferences and return a predefined JSON
    Schema that you will be provided.
5. Schema will contain 3 properties:
    (i) Score -> score you think resume deserves after taking into consideration Job Description, Resume, & User Preference.
    (ii) Pros -> good things you found about the candidate with respect to Job Description, Resume & User Profile
    (iii) Cons -> non-good things you found about the candidate with respect to Job Description, Resume & User Profile
"""


json_schema = {
  "type": "object",
  "properties": {
    "ai_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 10
    },
    "pros": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "cons": {
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["ai_score", "pros", "cons"]
}


def get_summarise_profile_prompt(top_cases_list):
    prompt = f"""
    You are a summarizer assistant.
    You will get cases in which the AI gave score to a particular resume with respect to a job description
    but the user disagreed with it and provided their reason / preference for that.

    There will be a list of dictionaries in which there will be cases of user disagreeing with an AI decision.
    In the same list there will be the reason(per case/dict) why user disagreed in that particular case.

    Your job is to summarise all that lists and create a User Profile which clearly reflects their preferences.

    The profile should be at max 150-200 words. And it should strictly include all important information about
    user's preferences while hiring.

    -----

    The list with various cases:
    {top_cases_list}
    """
    return prompt