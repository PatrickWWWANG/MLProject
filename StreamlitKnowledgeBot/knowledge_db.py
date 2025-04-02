from typing import List
import numpy as np
from openai_emb import OpenAIEmbedding
import json
import faiss

class EmbModel:
    def __init__(self, config):
        self.config = config
        if self.config['model_type'] == 'openai':
            self.model = OpenAIEmbedding(self.config)
        else:
            raise Exception(f'Model type: {self.config['model_type']} has not been implemented')
    
    def get_emb(self, texts):
        return self.model.get_emb(texts)
    
    def get_all_text_emb(self, texts, chuck_size=256):
        return self.model.get_all_text_emb(texts, chuck_size=chuck_size)
    
    def save_emb(self, text_list, text_emb, emb_file):
        self.model.save_emb(text_list, text_emb, emb_file)

class VectorDB:
    def __init__(self, emb_model):
        self.text2emb = {}
        self.id2text = []
        self.index = None
        self.emb_model = emb_model
    
    def load_emb(self, emb_file):
        with open(emb_file, 'r') as f:
            self.text2emb = json.load(f)
        emb_dim = len(next(iter(self.text2emb.values())))
        self.index = faiss.IndexFlatL2(emb_dim)
        for text, emb in self.text2emb.items():
            self.id2text.append(text)
            self.index.add(np.array(emb).reshape(1, -1).astype('float32'))
    
    def save_emb(self, emb_file):
        with open(emb_file, 'w') as f:
            json.dump(self.text2emb, f)
    
    def add_texts(self, texts, embs):
        for text, emb in zip(texts, embs):
            self.text2emb[text] = emb.tolist()
            self.id2text.append(text)
            self.index.add(np.array(emb).reshape(1, -1).astype('float32'))
            
    def query(self, text, topk):
        emb = self.emb_model.get_emb([text]).astype('float32')
        D, I = self.index.search(emb.reshape(1, -1), topk)
        return [self.id2text[i] for i in I[0]]
