import streamlit as st
from chat_model import ChatModel
from knowledge_db import EmbModel, VectorDB
from pdf_processor import extract_text_by_paragraph
from utils import save_uploaded_file
import os

st.title('Q&A Bot')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'assistant',
         'content': 'Hello, I am your Q&A bot. I can answer your question based on the file you uploaded.'}
    ]
    
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])
    
with st.sidebar:
    embedding_model = st.selectbox(
        'Select Embedding Model',
        ['text-embedding-3-small', 'text-embedding-ada-002', 'text-embedding-3-large'],
    )
    chat_model = st.selectbox('Choose Model', ['gpt-4o-mini', 'gpt-4o', 'o3-mini'])
    apikey = st.text_input('Input Your OpenAI API Key', type='password')
    uploaded_file = st.file_uploader('Choose a PDF file', type='pdf')
    
    if uploaded_file is not None:
        saved_file = save_uploaded_file(uploaded_file)
        if saved_file:
            paragraphs = extract_text_by_paragraph(saved_file)
            if paragraphs:
                emb_model = EmbModel({'model_type': 'openai', 'key': apikey})
                text_emb = emb_model.get_all_text_emb(paragraphs)
                emb_model.save_emb(paragraphs, text_emb, emb_file='./db/temp.json')
                st.success('Embeddings Extracted Successfully')
            else:
                st.write('No Text Extracted from the PDF')
            if os.path.exists(saved_file):
                os.remove(saved_file)
    else:
        st.stop()

# emb_model = EmbModel({'model_type': 'openai', 'key': apikey})
vector_db = VectorDB(emb_model)
vector_db.load_emb('./db/temp.json')
model = ChatModel(config={'openai-key': apikey, 'model': chat_model, 'model_type': 'openai'}, vector_db=vector_db)

if prompt := st.chat_input():
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)
    response = model.ask(prompt)
    st.session_state.messages.append({'role': 'assistant', 'content': response['response']})
    st.chat_message('assisstant').write(response['response'])
