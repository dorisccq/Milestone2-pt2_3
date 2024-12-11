from dotenv import load_dotenv
import os

load_dotenv()

from http import HTTPStatus
from dashscope import Application
import openai

def get_ans(question):
    response = Application.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
    app_id='ebbd49dff0ca44da806a4c728656c67d',
    prompt=f'{question}')

    if response.status_code != HTTPStatus.OK:
        print(f'request_id={response.request_id}')
        print(f'code={response.status_code}')
        print(f'message={response.message}')
        print(f'请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code')
    else:
        print(response.output.text)
        return response.output.text

api_key= os.getenv('OPENAI_API_KEY')

def llm_ans(question):
    messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': f'{question}'}
            ]
    
    
    client = openai.OpenAI(
        API_KEY = os.getenv('OPENAI_API_KEY')
        
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        max_completion_tokens=200,
        messages=messages
    )
    return response
def get_llm(text):
    url = 'https://api.dify.ai/v1'
