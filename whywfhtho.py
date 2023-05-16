import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

# Upload the first CSV file
st.header("Upload files")
uploaded_files = st.file_uploader("Choose 2 CSV file containing, 1) Score Key, and 2) Survey Results", type="csv", accept_multiple_files=True)

# Process the uploaded files
for uploaded_file in uploaded_files:
	if uploaded_file is not None:
		dataframe = pd.read_csv(uploaded_file)
		st.write(dataframe)
