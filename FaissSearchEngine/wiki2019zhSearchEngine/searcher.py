import faiss
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch
from transformers import BertTokenizer, BertModel

class Searcher:
    def __init__(self, index_path, mapping_path, title_path, model_name='uer/roberta-base-finetuned-chinanews-chinese'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.index = faiss.read_index(index_path)
        self.urls = self.load_url_mapping(mapping_path)
        self.titles = self.load_title_mapping(title_path)
        
    def load_url_mapping(self, mapping_path):
        with open(mapping_path, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file]
        return urls
    
    def load_title_mapping(self, title_path):
        with open(title_path, 'r', encoding='utf-8') as file:
            titles = [line.strip() for line in file]
        return titles
    
    def query_to_vector(self, query):
        inputs = self.tokenizer(query, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = self.model(**inputs)
        vector = outputs.pooler_output.detach().numpy()
        return vector
    
    def search(self, query, k=10):
        query_vector = self.query_to_vector(query)
        _, I = self.index.search(query_vector, k)
        results = []
        for i in I[0]:
            results.append([self.urls[i], self.titles[i]])
        return results
    
if __name__ == '__main__':
    searcher = Searcher('./data/wiki_zh.index', './data/wiki_map.txt', './data/wiki_title.txt')
    search_results = searcher.search('许嵩', k=30)
    for result in search_results:
        print(f'URL: {result[0]}, Title: {result[1]}')