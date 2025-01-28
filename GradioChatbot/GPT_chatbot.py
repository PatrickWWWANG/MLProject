import openai
import gradio as gr

def chat(user_message, history):
    openai.api_key = ' #API# '
    if not history:
        history = []
    
    messages = [{'role' : 'system', 'content' : 'You are a helpful assistant.'}]
    for user_ask, gpt_reply in history:
        messages.append({'role' : 'user', 'cnotent' : user_ask})
        messages.append({'role' : 'assistant', 'content' : gpt_reply})
        
    messages.append({'role' : 'user', 'content' : user_message})
    
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=messages
    )
    
    gpt_response = response.choices[0].message['content']
    history.append((user_message, gpt_response))
    
    return history, history

with gr.Blocks(theme='NoCrypt/miku') as demo:
    gr.Markdown("<h1 style='text-align: center;'>GPT-4o-mini Conversation WSC</h1>")
    chatbot = gr.Chatbot(elem_id='chat_window')
    message = gr.Textbox(label='Your message', placeholder='Type your message here', lines=2, elem_id='message_box', interactive=True)
    submit_button = gr.Button('Send')
    state = gr.State()
    submit_button.click(fn=chat, inputs=[message, state], outputs=[chatbot, state])
    
demo.launch(share=True)