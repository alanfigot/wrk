import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write(bytes_data)
