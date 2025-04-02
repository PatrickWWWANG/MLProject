from typing import Dict
from openai_model import OpenAI
from knowledge_db import VectorDB

class ChatModel:
    def __init__(self, config, vector_db):
        self.config = config
        if self.config['model_type'] == 'openai':
            self.model = OpenAI(config, vector_db)
        else:
            raise Exception(f'Model type: {self.config['model_type']} has not been implemented')
    
    def ask(self, question):
        return self.model.ask(question)
