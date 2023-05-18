import pandas as pd
import streamlit as st
import numpy as np
import re 

"""
# Persona Development  
"""
st.title(":red[_Under Construction_]")
st.divider()

# Create an empty placeholder
placeholder = st.empty()

# Upload CSV files
st.subheader("Upload a Score Key and Survey Results")
uploaded_files = st.file_uploader("Files must be in CSV format...", type="csv", accept_multiple_files=True)

if uploaded_files is not None and len(uploaded_files) > 2:
    st.warning("Please upload a maximum of 2 files. Only the first 2 files will be considered.")
    uploaded_files = uploaded_files[:2]
	
for uploaded_file in uploaded_files:
	df = pd.read_csv(uploaded_file)
	df.rename(columns=lambda x: x.strip(), inplace=True)
	print(df.columns)
	if any(string in df.columns for string in ['Identifier','Min','Max']):
		key = df
	# elif:
		# df[list(filter(lambda x: re.match(r'^F\d', x), df))[0]].dtype
	else: 
		results = df

# Process the uploaded files
if 'key' in locals() and 'results' not in locals():
	st.subheader(':blue[_Score Key_]')
	st.write(key, "Please upload Survey Responses")
		
# Process the uploaded files
elif 'results' in locals() and 'key' not in locals():
        st.subheader(':blue[_Survey Responses_]')
        st.write(results, "Please upload Survey Score Key")

elif 'results' and 'key' in locals():
	st.subheader(':blue[_Survey Score Key_]')
	st.write(key)
	
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
	st.write(results[['IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']].transpose())

	# st.subheader('Filters')
	# Create filter widgets
	# selected_columns = st.multiselect("Select columns", results.columns)
	# selected_rows = st.multiselect("Select rows", results.index)

	# Apply filters
	# filtered_df = results[selected_columns].loc[selected_rows]

	# Display filtered DataFrame
	# st.write(filtered_df)

	# Create a selectbox widget for column selection
	selected_column = st.selectbox("Select column for grouping",  list(filter(lambda x: re.match(r'^F\d', x), results)))

	# Group the DataFrame by the selected column and calculate the average
	grouped_df = results.groupby(selected_column).mean()

	# Display the grouped DataFrame
	st.write(grouped_df[['IC','SU','DQ','NP','TEAM','FUNC','EXPO','EXPE']])

else:
    placeholder.text("Please upload the necessary files")
