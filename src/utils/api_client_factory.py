import os
from openai import OpenAI

def get_client(model = 'openai'):
    if model == 'deepseek-chat':
        client = OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url=os.environ.get("DEEPSEEK_API_BASE"),
        )
    else:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE"),
        )
    return client
