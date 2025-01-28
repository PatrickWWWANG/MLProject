import openai
import requests
import gradio as gr
import random

openai.api_key = '# API #'

def chat_with_gpt(prompt, chat_log=None):
    response = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[
            {'role' : 'system', 'content' : 'You are a helpful assistant'},
        ] + chat_log + [{'role' : 'user', 'content' : prompt}],
        temperature=0.7,
        max_tokens=120
    )
    return response['choices'][0]['message']['content'].strip()

# chat_log = []

# for _ in range(3):
#     user_input = input('You: ')
#     gpt_response = chat_with_gpt(user_input, chat_log)
#     chat_log.extend([
#         {'role' : 'user', 'content' : user_input},
#         {'role' : 'assistant', 'content' : gpt_response}
#     ])
#     print(f'ChatGPT: {gpt_response}')
#     print()


# # Gradio Global State

# scores = []

# def track_score(score):
#     scores.append(score)
#     top_scores = sorted(scores, reverse=True)[: 3]
#     return top_scores

# demo = gr.Interface(
#     fn=track_score,
#     inputs=gr.Number(label='Score'),
#     outputs=gr.JSON(label='Top 3 Scores')
# )
# demo.launch()


# Gardio Session State

def chat(message, history):
    history = history or []
    message = message.lower()
    if message.startswith('How many'):
        response = random.randint(1, 10)
    elif message.startswith('How'):
        response = random.choice(['Great', 'Good', 'Okay', 'Bad'])
    elif message.startswith('Where'):
        response = random.choice(['Here', 'There', 'Somewhere'])
    else:
        response = "I don't know"
    history.append((message, response))
    return history, history

chatbot = gr.Chatbot()
demo = gr.Interface(
    fn=chat,
    inputs=['text', 'state'],
    outputs=[chatbot, 'state'],
    allow_flagging='never'
)
demo.launch()