from tenacity import retry, stop_after_attempt, wait_fixed
import numpy as np
import requests
import json
from tqdm import tqdm
from utils import write_json_file

class OpenAIEmbedding:
    def __init__(self, config):
        self.config = config
        self.key = self.config['key']
        self.url = self.config.get('url', 'https://api.openai.com/v1/embeddings')
    
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
    def get_emb(self, texts):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
        payload = {
            'model': 'text-embedding-ada-002',
            'input': texts
        }
        response = requests.post(
            self.url, headers=headers, json=payload, stream=False, timeout=180
        )
        response = json.loads(response.text)
        
        emb_array = []
        for i in range(len(response['data'])):
            emb_array.append(response['data'][i]['embedding'])
        return np.array(emb_array)

    def get_all_text_emb(self, texts, chuck_size=256):
        text_emb = []
        for i in tqdm(range(0, len(texts), chuck_size)):
            temp_emb = self.get_emb(texts[i : i + chuck_size])
            text_emb.append(temp_emb)
        text_emb = np.concatenate(text_emb)
        return text_emb
    
    def save_emb(self, text_list, text_emb, emb_file):
        text2emb = {}
        for i in range(len(text_list)):
            text2emb[text_list[i]] = text_emb[i].tolist()
        write_json_file(text2emb, emb_file)
