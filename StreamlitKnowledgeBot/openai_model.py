import openai
from typing import Dict
from tenacity import retry, stop_after_attempt, wait_fixed
from knowledge_db import VectorDB

class OpenAI:
    def __init__(self, config, vector_db):
        self.config = config
        self.vector_db = vector_db
        openai.api_key = self.config.get('openai-key')
    
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
    def ask(self, question):
        res = self.vector_db.query(question, topk=5)
        messages = [{
            'role': 'user',
            'content': f'Please answer the question based on the reference material I provide. Be aware, \
            you should only answer based on the reference material. If the reference material cannot lead \
            to answer, tell me you do not know. The reference material is: {res} \n My question is: {question} '
        }]
        response = openai.ChatCompletion.create(model=self.config.get('model', 'gpt-4o-mini'), messages=messages)
        msg = response.choices[0].message.content
        return {
            'response': msg,
            'knowledge': res
        }
