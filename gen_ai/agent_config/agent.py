import os
from langchain_mistralai import ChatMistralAI
from langchain.agents import create_agent
from gen_ai.agent_config.tools import get_user_profile
from langchain_core.messages import SystemMessage, HumanMessage
from gen_ai.prompts import system_prompt


MODEL_ID = os.getenv("MODEL_ID")

tools_list = [get_user_profile]

CLIENT = ChatMistralAI(model = MODEL_ID, temperature = 0)

AGENT = create_agent(CLIENT, tools = tools_list)


def invoke_agent(user_prompt):
    messages = [
        SystemMessage(content = system_prompt),
        HumanMessage(content = user_prompt)
    ]

    response = AGENT.invoke({'messages': messages})

    return response["messages"][-1].content