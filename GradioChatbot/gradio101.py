import gradio as gr
import numpy as np
from PIL import Image

def greet(name):
    return f'Hello, {name}'

# iface = gr.Interface(fn=greet, inputs='text', outputs='text')
# iface.launch()


# Input types

def echo(input_text):
    return "Your input: " + input_text

# # Text input
# iface = gr.Interface(fn=echo, inputs='text', outputs='text')
# iface.launch

def square(x):
    return x ** 2

# # Number input
# iface = gr.Interface(fn=square, inputs='number', outputs='number')
# iface.launch

def age_advice(age):
    if age < 18:
        return 'You are young!'
    elif age < 60:
        return 'Enjoy your best years!'
    else:
        return 'Age is just a number!'
    
# # Slider input
# iface = gr.Interface(fn=age_advice, inputs=gr.Slider(0, 100), outputs='text')
# iface.launch()

def cat_lover(is_lover):
    return 'Cat lover are welcome!' if is_lover else 'Not a cat person, I see.'

# # Checkbox input
# iface = gr.Interface(fn=cat_lover, inputs='checkbox', outputs='text')
# iface.launch()

def season_description(season):
    descriptions = {
        'Spring' : 'Spring is good!',
        'Summer' : 'Summer is good!',
        'Autumn' : 'Autumn is good!',
        'Winter' : 'Winter is good!',
    }
    return descriptions[season]

# # Radio input
# iface = gr.Interface(fn=season_description, inputs=gr.Radio(['Spring', 'Summer', 'Autumn', 'Winter']), outputs='text')
# iface.launch()

def language_info(language):
    info = {
        'Python' : 'Good language!',
        'Java' : 'Good language!',
        'C++' : 'Good language!',
    }
    return info[language]

# # Dropdown input
# iface = gr.Interface(fn=language_info, inputs=gr.Dropdown(['Python', 'Java', 'C++']), outputs='text')
# iface.launch()


# Output types

def reverse_string(text):
    return text[::-1]

# # Text output
# iface = gr.Interface(fn=reverse_string, inputs='text', outputs='text')
# iface.launch()

def sentiment_analysis(text):
    sentiment = 'Positive' if 'happy' in text else 'Negative'
    return sentiment

# # Label output
# iface = gr.Interface(fn=sentiment_analysis, inputs='text', outputs='label')
# iface.launch()

def to_grayscale(input_image):
    image = Image.fromarray(input_image.astype('uint8'), 'RGB')
    grayscale_image = image.convert('L')
    return np.array(grayscale_image)

# # Image output
# iface = gr.Interface(fn=to_grayscale, inputs='image', outputs='image')
# iface.launch()


# Custom components

def greet(name):
    return 'Hello ' + name + '!'

# with gr.Blocks() as demo:
#     name = gr.Textbox(label='Name')
#     output = gr.Textbox(label='Output Box')
#     greet_btn = gr.Button('Greet')
#     greet_btn.click(fn=greet, inputs=name, outputs=output)
# demo.launch()


# Multiple inputs and outputs

def greet(name, is_morning, temperature):
    salutation = 'Good morning' if is_morning else 'Good evening'
    greeting = f'{salutation} {name}. It is {temperature} degrees today.'
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

# demo = gr.Interface(
#     fn=greet,
#     inputs=['text', 'checkbox', gr.Slider(0, 100)],
#     outputs=['text', 'number'],
# )
# demo.launch()


# Dynamic interface

def calculator(num1, operation, num2):
    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        return num1 / num2
    
iface = gr.Interface(
    fn=calculator,
    inputs=['number', gr.Radio(['add', 'subtract', 'multiply', 'divide']), 'number'],
    outputs='number',
    live=True,
)
iface.launch()