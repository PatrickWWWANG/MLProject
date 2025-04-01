import time
import streamlit as st
from code_agent import CodeAgent
from loguru import logger
import io

log_stream = io.StringIO()

class StreamlitSink:
    def write(self, message):
        log_stream.write(message)
    
    def flush(self):
        pass

logger.remove()
logger.add(StreamlitSink(), format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}')

def update_log():
    while True:
        if 'log_text_area' in st.session_state:
            st.session_state.log_content = log_stream.getvalue()
            
if 'log_content' not in st.session_state:
    st.session_state.log_content = ''
    st.session_state.last_log_update = time.time()

if 'test_case' not in st.session_state:
    st.session_state['test_case'] = []

with st.sidebar:
    st.title('Configuration')
    selected_model = st.selectbox('Choose Model', ['gpt-4o-mini', 'gpt-4o', 'o3-mini'])
    apikey = st.text_input('Input Your OpenAI API Key', type='password')
    
if apikey:
    agent = CodeAgent(openai_key=apikey, model=selected_model)
else:
    st.error('Please Input Your API Key in Sidebar.')
    st.stop()

st.title('Code Agent')

question = st.text_area('Input Your Code Problem: ', height=300)

st.write('Add Test Case:')
input_cols, output_cols = st.columns(2)
with input_cols:
    test_input = st.text_area('Input: ', height=100, key='test_input')
with output_cols:
    test_output = st.text_area('Expected Output', height=100, key='test_output')

add_test_case, clear_test_case = st.columns(2)
with add_test_case:
    if st.button('Add Test Case'):
        st.session_state['test_case'].append([test_input.strip(), test_output.strip()])
        st.success('Test Case Added')
with clear_test_case:
    if st.button('Clear All Test Cases'):
        st.session_state['test_case'] = []
        st.warning('All Test Cases Cleared')

st.write('Added Test Case: ')
for i, test in enumerate(st.session_state['test_case']):
    st.text(f'Test Case {i + 1}: \n Input: \n{test[0]} \nExpected Output: \n{test[1]}')
    
if st.button('Generate Code'):
    for case in st.session_state['test_case']:
        agent.add_testcase(case[0], case[1])
    
    flag = agent.run_pipeline(question)
    
    current_time = time.time()
    if current_time - st.session_state.last_log_update > 1:
        st.session_state.log_content = log_stream.getvalue()
        st.session_state.last_log_update = current_time
    
    st.markdown('## Agent Log')
    st.markdown(st.session_state.log_content)
    
    if hasattr(agent, 'generated_code'):
        if flag:
            st.success('Code Agent Solved the Problem')
        else:
            st.error('Code Agent cannot Solve the Problem')
        st.markdown('## Final Result')
        st.code(agent.generated_code, language='python')
