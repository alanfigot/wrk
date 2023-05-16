from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Persona Development

If you have any questions... 

"""

upload1 = st.file_uploader("Upload your file here...", type=['csv'])

if upload1 is not None:
	ScoreKey = pd.read_csv(upload1)
	st.write(ScoreKey)
	
upload2 = st.file_uploader("Upload your file here...", type=['csv'])

if upload2 is not None:
	SurveyResults = pd.read_csv(upload2)
	st.write(SurveyResults)
