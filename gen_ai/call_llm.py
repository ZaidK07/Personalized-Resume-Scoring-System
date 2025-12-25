from mistralai import Mistral
import os

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
model = os.getenv("MODEL_ID")

client = Mistral(api_key = api_key)

def invoke_model(model_prompt):
    response = client.chat.complete(
        model = model,
        messages = [{
            'role': 'user',
            'content': model_prompt
        }],
        temperature = 0,
        max_tokens = 1024
    )
    print("Total Tokens(call_llm.invoke_model)-->",response.usage.total_tokens)
    return response.choices[0].message.content



if __name__ == '__main__':
    response = invoke_model(model_prompt = "Hello there!")
    print(response)