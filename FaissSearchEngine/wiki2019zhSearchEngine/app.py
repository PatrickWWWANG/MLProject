import streamlit as st
from searcher import Searcher

searcher = Searcher('./data/wiki_zh.index', './data/wiki_map.txt', './data/wiki_title.txt')
st.title('My Wiki Search Engine')
query = st.text_input('Input Your Query', '')

if query:
    results = searcher.search(query, k=15)
    if results:
        st.subheader('Search Result')
        for result in results:
            st.write(f'URL: {result[0]}, Title: {result[1]}')
    else:
        st.write('No Result Found')