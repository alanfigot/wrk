import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

# Upload CSV files
st.header("Upload CSV files")
uploaded_files = st.file_uploader("Choose the 1) Score Key, and 2) Survey Results", type="csv", accept_multiple_files=True)

# Process the uploaded files
for uploaded_file in uploaded_files[0:1]:
	st.subheader('Persona Development _Score Key_ :blue[!!] :sunglasses:')
	if uploaded_file is not None:
		ScoreKey = pd.read_csv(uploaded_file)
		st.write(ScoreKey)
		
# Process the uploaded files
for uploaded_file in uploaded_files[1:2]:
	st.subheader('Persona Development :blue[_Survey Results_] :sunglasses:')
	if uploaded_file is not None:
		SurveyResults = pd.read_csv(uploaded_file)
		st.write(SurveyResults)
