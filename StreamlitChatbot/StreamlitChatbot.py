import openai
import streamlit as st

# with st.sidebar:
#     openai.api_key = st.text_input('API Key', key='chatbot_api_key', type='password')

st.title('ChatBot')
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role' : 'assistant', 'content' : 'How can I help you?'}]
    
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

prompt = st.chat_input
if prompt:
    openai.api_key = ' #API# '
    st.session_state.messages.append({'role' : 'user', 'content' : prompt})
    st.chat_message('user').write(prompt)
    response = openai.ChatCompletion.create(model='gpt-4o-mini', message=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message('assisstant').write(msg.content)