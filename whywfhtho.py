import pandas as pd
import streamlit as st
import numpy as np

"""
# Persona Development

If you have any questions... 

"""

chart_data = pd.DataFrame(np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)


