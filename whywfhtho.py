import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

# Upload the first CSV file
st.header("Upload the first CSV file")
file_1 = st.file_uploader("Choose a CSV file", type="csv")
    
# Upload the second CSV file
st.header("Upload the second CSV file")
file_2 = st.file_uploader("Choose a CSV file", type="csv")

# Process the uploaded files
if file_1 and file_2:
    df_1 = pd.read_csv(file_1)
    df_2 = pd.read_csv(file_2)

# Display the contents of the first CSV file
st.subheader("Contents of the first CSV file:")
st.write(df_1)

# Display the contents of the second CSV file
st.subheader("Contents of the second CSV file:")
st.write(df_2)

