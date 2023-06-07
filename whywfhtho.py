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
uploaded_files = st.file_uploader("Files must be in .CSV or .XLSX format...", type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files is not None and len(uploaded_files) > 3:
    st.warning("Please upload a maximum of 3 files. Only the first 3 files will be considered.")
    uploaded_files = uploaded_files[:3]

for uploaded_file in uploaded_files:
	if uploaded_file:
		filename = uploaded_file.name
		if filename.endswith('.csv') == True:
			df = pd.read_csv(uploaded_file, index_col=False)
		else:
			df = pd.read_excel(uploaded_file)
		df.rename(columns=lambda x: x.strip(), inplace=True)
		# Identify Score Key File 
		if all(string in df.columns for string in ['Identifier','Min','Max']): #any?     
			key = df 
			key['Identifier'].fillna('', inplace=True)
			key = key[key['Identifier'].str.startswith('P')]
			key = key.reset_index(drop=True)
			for i in ['Min','Max']: 
				key[i].fillna(0, inplace=True)

		# Identify Results
		else:
			f1 = list(filter(lambda x: re.match(r'^P\d', x), df))[0]
			if np.issubdtype(df[f1].dtype, np.number):
				results = df
		# Identify Values
			else:
				labels = df

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
	results = results.filter(regex='^P')
	# Convert columns to numeric, dropping the ones that cannot be converted
	numeric_columns = []
	for column in results.columns:
		try:
			results[column] = pd.to_numeric(results[column])
			numeric_columns.append(column)
		except ValueError:
			pass

	# Create a new DataFrame with the numeric columns
	results = results[numeric_columns]
	st.write(results)
	
	# Create new columns for scores 
	totals = pd.DataFrame(columns=['IC','SU','DQ','NP','Teamwork','Functionality','Exposure','Experience'])
	# len(results.index)
	
	# Calculate Scores 
	valid_columns = key['Identifier'].unique()

	for dimension in totals.columns:
		temp_results = results.copy()
		for col in temp_results.columns:
			if col in valid_columns:
				key_match = key.loc[key['Identifier'] == col]
				if not key_match.empty:
					minimum = key_match['Min'].values[0]
					maximum = key_match['Max'].values[0]

					if minimum != maximum and maximum > minimum:
						fraction = 1 / (maximum - minimum)
					else:
						fraction = 0
				if key.loc[key['Identifier'] == col, dimension].values[0] == 'Min':
					temp_results[col] = temp_results[col].apply(lambda x: (1 -( (x - minimum) * fraction)))
				
				elif key.loc[key['Identifier'] == col, dimension].values[0] == 'Max':
					temp_results[col] = temp_results[col].apply(lambda x: ( (x - minimum) * fraction))
				else:
					temp_results[col] = temp_results[col].apply(lambda x: x * 0)
			else:
				temp_results[col] = temp_results[col].apply(lambda x: x * 0)
		totals[dimension] = temp_results.sum(axis=1)

	# Max Possible 
	max_out = key.copy()
	for dimension in ['IC', 'SU','DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']:
		for condition, column in {'Max': 'Max', 'Min': 'Min'}.items():
			mask = max_out[dimension] == condition
			max_out.loc[mask, dimension] = max_out.loc[mask, column]
		
	max_out = max_out[['Identifier','IC', 'SU','DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']]
	max_out.set_index('Identifier', inplace=True)
	max_out = max_out.transpose()
	
	# Convert columns to numeric, dropping the ones that cannot be converted
	numeric_columns = []
	for column in max_out.columns:
		try:
			max_out[column] = pd.to_numeric(max_out[column])
			numeric_columns.append(column)
		except ValueError:
			pass

	# Create a new DataFrame with the numeric columns
	max_out = max_out[numeric_columns]
	
	max_out.replace('', np.nan, inplace=True)  # Replace empty strings with NaN values
	max_out.dropna(axis=1, how='all', inplace=True)
	
	max_totals = pd.DataFrame(columns=['IC','SU','DQ','NP','Teamwork','Functionality','Exposure','Experience'])
	
	valid_columns = key['Identifier'].unique()

	# Calculate Max Score 
	for dimension in max_totals.columns:
		temp_results = max_out.copy()
		for col in temp_results.columns:
			if col in valid_columns:
				key_match = key.loc[key['Identifier'] == col]
				if not key_match.empty:
					minimum = key_match['Min'].values[0]
					maximum = key_match['Max'].values[0]
					if minimum != maximum and maximum > minimum:
						fraction = 1 / (maximum - minimum)
					else:
						fraction = 0
				if key.loc[key['Identifier'] == col, dimension].values[0] == 'Min':
					temp_results[col] = pd.to_numeric(temp_results[col], errors='coerce')
					temp_results[col] = temp_results[col].apply(lambda x: (1 -( (x - minimum) * fraction)))
				elif key.loc[key['Identifier'] == col, dimension].values[0] == 'Max':
					temp_results[col] = pd.to_numeric(temp_results[col], errors='coerce')
					temp_results[col] = temp_results[col].apply(lambda x: ( (x - minimum) * fraction))
				else:
					temp_results[col] = temp_results[col].apply(lambda x: x * 0)
			else:
				temp_results[col] = temp_results[col].apply(lambda x: x * 0)

		max_totals[dimension] = temp_results.sum(axis=1)
	
	max_totals = max_totals[['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']]

	for col in ['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']:
		max_score = max_totals[col][col]
		totals[col] = totals[col].apply(lambda x: x / max_score)

	st.subheader(':blue[_Analysis Results_] :sunglasses:')
	st.write(totals.style.format("{:.2}"))
	
	# Create a selectbox widget for column selection
	if 'Filter' in key.columns:
		filters = [item for item in list(key['Filter'].unique()) if str(item) != '']
	# else: 
	#	filters = [item for item in list(key['Identifier'].unique()) if str(item) != '']
		
		selected_filter = st.selectbox("Select filter for grouping", filters)
		selected_filter_id = (key.loc[key['Filter']==selected_filter]['Identifier']).values[0]
		
		filtered_results = results.join(totals).groupby(selected_filter_id).mean()
	
		if 'labels' in locals():
			tags = {}
			if len(labels[selected_filter_id].unique()) == len(results[selected_filter_id].unique()):
				for i in range(len(labels[selected_filter_id].unique())):
					tags[results[selected_filter_id].unique()[i]] = labels[selected_filter_id].unique()[i].strip()
			filtered_results = filtered_results[['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']].rename(index=tags)
			st.write(filtered_results.style.format("{:.2}"))
		else: 
			filtered_results = filtered_results[['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']]
			st.write(filtered_results.style.format("{:.2}"))
	
	# Download Options
	selected_file = st.selectbox("Select file to download", ['Individual Scores','Group Scores'])
	download_df = totals
	btn =  "Download Individual Scores"
	if selected_file == 'Group Scores':
		download_df = filtered_results
		btn =  f"Download Scores by {selected_filter}" 
	
	st.download_button(
		label = btn, 
		data = download_df.to_csv().encode('utf-8'), 
		file_name= "totals.csv",
		mime="text/csv",
		key='download-csv')
else:
    placeholder.text("Please upload the necessary files")
