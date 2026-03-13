import streamlit as st
import pandas as pd
from statsbombpy import sb

st.set_page_config(page_title="Planets", layout="wide")

df = pd.read_excel("planets.xlsx")

df

st.scatter_chart(df, 
                 x='Distance from Sun (106km)', 
                 y='Mass (1024kg)',#'Length of day (Hours)',
                 color='Planet',
                 #size='Mass (1024kg)',
                 )
