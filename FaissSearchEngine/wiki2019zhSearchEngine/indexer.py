import faiss
import numpy as np
import pandas as pd
from tqdm import tqdm
import torch
from transformers import BertTokenizer, BertModel

class Indexer:
    def __init__(self, model_name='uer/roberta-base-finetuned-chinanews-chinese', batch_size=8):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name).to(self.device)
        self.index = faiss.IndexFlatL2(768) # Vector size of BERT
        self.batch_size = batch_size
        self.url_mapping = []
        self.title_mapping = []
        
    def texts_to_vectors(self, texts):
        vectors = []
        for i in tqdm(range(0, len(texts), self.batch_size)):
            batch_texts = texts[i : i + self.batch_size].tolist()
            inputs = self.tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True, max_length=512)
            inputs = {k : v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            batch_vectors = outputs.pooler_output.detach().cpu().numpy()
            vectors.extend(batch_vectors)
        return np.array(vectors)
    
    def add_to_index(self, texts, urls, titles):
        vectors = self.texts_to_vectors(texts)
        self.index.add(vectors)
        self.url_mapping.extend(urls)
        self.title_mapping.extend(titles)
    
    def save_index_and_mapping(self, index_path, mapping_path, title_path):
        faiss.write_index(self.index, index_path)
        with open(mapping_path, 'w', encoding='utf-8') as f:
            for url in self.url_mapping:
                f.write(url + '\n')
        with open(title_path, 'w', encoding='utf-8') as f2:
            for title in self.title_mapping:
                f2.write(str(title) + '\n')
                
    def build_index_from_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path)
        self.add_to_index(df['content'], df['url'], df['title'])
        
if __name__ == '__main__':
    indexer = Indexer()
    indexer.build_index_from_csv('./data/wiki_zh.csv')
    indexer.save_index_and_mapping('./data/wiki_zh.index', './data/wiki_map.txt', './data/wiki_title.txt')
