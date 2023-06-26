import pandas as pd
import streamlit as st
import numpy as np
import re
import openpyxl 
import plotly.express as px

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
		if all(string in df.columns for string in ['Identifier','Questions','Min','Max']): #any?     
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

# Show which files exist
if 'key' in locals() and 'labels' in locals() and 'results' in locals():
	pass 

elif 'key' in locals() and 'results' in locals() and 'labels' not in locals():
	st.write("Please remember to upload Survey Label Responses")
	pass

elif 'key' in locals() and 'results' not in locals():
	st.subheader(':blue[_Survey Score Key_]')
	st.write(key)
	if 'labels' in locals():
		st.subheader(':blue[_Survey Label Responses_]')
		st.write(labels)
	st.write("Please upload Survey Value Responses")

elif 'key' not in locals() and 'results' in locals():
	st.subheader(':blue[_Survey Value Responses_]')
	st.write(results)
	if 'labels' in locals():
		st.subheader(':blue[_Survey Label Responses_]')
		st.write(labels)
	st.write("Please upload Survey Score Key")

elif 'key' not in locals() and 'results' not in locals() and 'labels' in locals():
	st.subheader(':blue[_Survey Label Responses_]')
	st.write(labels)
	st.write("Please upload Survey Score Key and Survey Value Responses")
	
if 'results' in locals() and 'key' in locals():
	# results = results.filter(regex='^P')
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
	st.write("Make sure all scores in the table above are between 0 and 1")

	# Create a selectbox widget for column selection
	if 'Filter' in key.columns:
		filters = [item for item in list(key['Filter'].unique()) if str(item) not in ['',np.nan,'nan',0,float('NaN')]]
	# else: 
	#	filters = [item for item in list(key['Identifier'].unique()) if str(item) not in ['',np.nan,'nan',0,float('NaN')]]
		
		selected_filter = st.selectbox("Select filter for grouping", filters)
		selected_filter_id = (key.loc[key['Filter']==selected_filter]['Identifier']).values[0]
		
		if 'labels' in locals():
			filtered_results = labels[key[key['Filter']==selected_filter]['Identifier'].values].join(totals).groupby(selected_filter_id).mean()
			st.write(filtered_results.style.format("{:.2}"))
		elif 'results' in locals(): 
			filtered_results = results.join(totals).groupby(selected_filter_id).mean()
			filtered_results = filtered_results[['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']]
			st.write(filtered_results.style.format("{:.2}"))
	
	st.subheader(':blue[_Data Visualization_] ')

	if 'labels' in locals():
		score = labels.join(totals)
		score.fillna('', inplace=True)
	else: 
		score = results.join(totals)
		score.fillna('', inplace=True)

	# graphic = st.radio("Select one of the following options:",('Scatter', 'Bar', 'Distribution', 'Box'))

	variable1 = st.selectbox("Main Variable: ",list([''] + ['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience'])) 
	variable2 = st.selectbox("Secondary Variable: ",list([''] + ['IC', 'SU', 'DQ', 'NP', 'Teamwork','Functionality','Exposure','Experience']))
	
	variable3 = st.selectbox('Color by',list([''] + [x for x in key['Filter'].unique() if x not in [np.nan]]))
	variable3_id = ''
	if variable3 != '':
		variable3_id = key[key['Filter']==variable3]['Identifier'].values[0]

	if variable1 != '' and variable2 != '' and variable3 != '': 		
		
		# Scatter
		fig1 = px.scatter(score, x=variable1, y=variable2, color=variable3_id)
		fig1.update_layout(title_text=f'{variable1} Score by {variable2}')

		# Distribution 
		fig2 = px.histogram(score, x=variable1, color=variable3_id, hover_data=score.columns)
		fig2.update_layout(title_text=f'{variable1} Color by {variable3}')

		# Bar Plot
		temp = score.groupby(variable3_id).mean().sort_values(variable1, ascending=False)
		if len(score[variable3_id].unique())>10:
			temp = pd.concat([temp.head(5),temp.tail(5)])
    
		fig3 = px.bar(temp, y = ['IC','SU','NP','DQ'], barmode='group')
		if len(score[variable3_id].unique())>10:
    			fig3.update_layout(title_text=f"{variable1} Scores <br> <sup >Note that categories have been reduced to top 5 and bottom 5 {variable1} scored by {variable3} </sup>") 
		else: 
    			fig3.update_layout(title_text=f'{variable1} Scores')
	
		
		tab1, tab2, tab3 = st.tabs(["Scatter", "Distribution", "Bar"]) # "Violin"
		with tab1:
			st.plotly_chart(fig1, theme='streamlit', use_container_width=True)
		with tab2:
			st.plotly_chart(fig2, theme='streamlit', use_container_width=True)
		with tab3:
			st.plotly_chart(fig3, theme='streamlit', use_container_width=True)
	else:
		st.write("Please select all variables")
			


	# else: 
	#		# Scatter
	#		fig1 = px.scatter(score, x=variable1, y=variable2) 
	#		# Histogram
	#		fig2 = px.histogram(score, x=variable1, hover_data=score.columns)


	# Download Options
	st.subheader(':blue[_Download Data_] ')
	
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
