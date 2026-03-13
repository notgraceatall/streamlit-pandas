import streamlit as st
import pandas as pd
from statsbombpy import sb

st.set_page_config(page_title="TV", layout="wide")

df = pd.read_excel("tv.xlsx")

df

st.bar_chart(df,
             x="Programme",
             y=["TV set", "PC/Laptop", "Tablet", "Smartphone"],
             height=400,
             horizontal = True,
             use_container_width=True)
