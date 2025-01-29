import streamlit as st
import pandas as pd

# st.title('First Streamlit Application')
# st.write('Welcome to Streamlit')

# name = st.text_input('Put your name')
# age = st.slider('Choose your age', 0, 100, 25)
# st.write(f'Hello, {name}! Your age is {age}.')

data = {'Name' : ['Jack', 'John', 'Amy'],
        'Age' : [25, 26, 18]}
df = pd.DataFrame(data)
# st.write(df)


# # Streamlit Slidebar
# sidebar_input = st.sidebar.text_input('Input Your Content')
# sidebar_slider = st.sidebar.slider('Pick a Number', 0, 100)

# # Caching
# @st.chche_data # Decorator
# def load_data():
#     data = pd.read_csv('large_dataset.csv')
#     return data

# data = load_data()
# st.write(data)

# # Upload file
# uploaded_file = st.file_uploader('Choose a file')
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)
#     st.write(df)
    
# # Plot lib
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.scatter([1, 2, 3], [1, 2, 3])
# st.pyplot(fig)

# import plotly.express as px
# df = pd.DataFrame({
#     'x' : [1, 2, 3, 4],
#     'y' : [10, 11, 12, 13]
# })
# fig = px.line(df, x='x', y='y')
# st.plotly_chart(fig)

# # Progress bar and state information
# import time
# progress_bar = st.progress(0)
# for i in range(100):
#     progress_bar.progress(i + 1)
#     time.sleep(0.1)
# st.success('Success!')

# # Layout control
# tab1, tab2 = st.tabs(['First Tab', 'Second Tab'])
# with tab1:
#     st.header('This is first tab')
# with tab2:
#     st.header('This is second tab')

# # Custom theme
# st.markdown(
#     """
#     <style>
#     .big-font {
#         font-size:50px !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown('<p class="big-font">This is big font</p>', unsafe_allow_html=True)
