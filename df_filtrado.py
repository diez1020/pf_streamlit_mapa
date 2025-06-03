import streamlit as st 
import pandas as pd 

df = pd.read_csv('all_seasons.csv').head(2000)

st.dataframe(df)