import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""
dataframe1 = []
dataframe2 = []

# Upload the first CSV file
st.header("Upload files")
uploaded_files = st.file_uploader("Choose 2 CSV file containing, 1) the Score Key, and 2) Survey Results", type="csv", accept_multiple_files=True)

# Process the uploaded files
for i in range len(uploaded_files):
	print(i)
	# if uploaded_file is not None:
	# 	dataframe = pd.read_csv(uploaded_file)
	#	st.write(dataframe)
