from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

uploaded_file = st.file_uploader("Upload your file here...", type=['csv'])

if uploaded_file is not None:
	dataframe = pd.read_csv(uploaded_file)
	st.write(dataframe)
