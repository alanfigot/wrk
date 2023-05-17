import pandas as pd
import streamlit as st
import numpy as np

"""
# Persona Development (Not Working Anymore!) 

If you have any questions... 

"""
# Upload CSV files
st.header("Upload CSV files")
uploaded_files = st.file_uploader("Choose the 1) Score Key, and 2) Survey Results", type="csv", accept_multiple_files=True)

if uploaded_files is not None and len(uploaded_files) > 2:
    st.warning("Please upload a maximum of 2 files. Only the first 2 files will be considered.")
    uploaded_files = uploaded_files[:2]
	
for uploaded_file in uploaded_files:
	df = pd.read_csv(uploaded_file)
	df = df.rename(columns=lambda x: x.strip(), inplace=True)
	if any(string in df.columns for string in ['Identifier','Min','Max']):
		key = uploaded_file
	else: 
		results = uploaded_file

# Process the uploaded files
st.subheader(':blue[_Score Key_]')
st.write(key)
		
# Process the uploaded files
st.subheader(':blue[_Survey Responses_]')
st.write(results)

results = results.filter(regex='^(F|X)')
for i in ['Identifier','IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']: 
    key[i].fillna('', inplace=True)

key = key[key['Identifier'].str.startswith(('F','X'))]

for i in ['IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']: 
    results[i] = 0

for col in ['IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']:
    for Qid in key[key[col].str.contains(('Min|Max'))]['Identifier']:
        if Qid in results.columns:
            minimum = key.loc[key['Identifier'] == Qid, 'Min'].values[0]
            maximum = key.loc[key['Identifier'] == Qid, 'Max'].values[0]
            fraction = 1 / (maximum-minimum)
            if key.loc[key['Identifier'] == str(Qid), col].str.strip().eq("Min").any():
                results[col] = results[col] + (1 -((results[Qid]-minimum)* fraction))
            if key.loc[key['Identifier'] == str(Qid), col].str.strip().eq("Max").any():
                results[col] = results[col] + ((results[Qid]-minimum)* fraction)

st.subheader(':blue[_Analysis Results_] :sunglasses:')
st.write(results[['IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']])

