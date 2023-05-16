import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

# Upload the first CSV file
st.header("Upload both CSV files: 1) ScoreKey 2) Survey Results")
uploaded_files = st.file_uploader("Choose a CSV file", type="csv", accept_multiple_files=True)

# Process the uploaded files
for uploaded_file in uploaded_files:
	if uploaded_file is not None:
		dataframe = pd.read_csv(uploaded_file)
		st.write(dataframe)
