from together import Together
from mistralai import Mistral
from langchain_anthropic import ChatAnthropic

import os


def get_response_llama(question):
    client = Together(api_key="apikey")
    
    instruction = "Обери правильну відповідь і поверни одну із букв (А, Б, В, Г чи Д) без додаткових символів\n"

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=[
            {
                    "role": "user",
                    "content": f"{question}\n{instruction}"
            }
    ],
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True
    )

    # for token in response:
    #     if hasattr(token, 'choices'):
    #         print(token.choices[0].delta.content, end='', flush=True)
    
    return list(response)[0].choices[0].delta.content


def get_response_mistralai(question):
    api_key = "apikey"
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    instruction = "Обери правильну відповідь і поверни одну із букв (А, Б, В, Г чи Д) без додаткових символів\n"

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": f"{question}\n{instruction}"
            },
        ]
    )
    return chat_response.choices[0].message.content


# Define the function using ChatAnthropic
def get_response_claude(question):
    # Replace "..." with your actual Anthropic API key
    api_key = "sk-ant-"  
    
    # Initialize the Claude model
    model = ChatAnthropic(
        model="claude-3-5-sonnet-20240620", 
        temperature=0, 
        anthropic_api_key=api_key
    )

    # Instruction to guide the response
    instruction = "Обери правильну відповідь і поверни одну із букв (А, Б, В, Г чи Д) без додаткових символів і пояснень\n"
    
    # Prepare the prompt
    prompt = f"{question}\n{instruction}"
    
    # Generate a response
    response = model.invoke([{"role": "user", "content": prompt}])
    
    # Return the content of the response
    return response.content

