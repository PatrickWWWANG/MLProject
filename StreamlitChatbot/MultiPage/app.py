import streamlit as st
from Pages.page1 import show_page1
from Pages.page2 import show_page2

st.title("Multi Page Streamlit Application")

# Sidebar for navigation
page = st.sidebar.selectbox("Select a page", ["Page1", "Page2"])

# Display the selected page
if page == "Page1":
    show_page1()
elif page == "Page2":
    show_page2()
