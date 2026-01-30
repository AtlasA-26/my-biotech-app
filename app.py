import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Atlas Agentic")

DATA_PATH = "data/research_data.csv"

@st.cache_data(ttl=3600)
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()

st.title("🔬 Atlas Agentic Intel")
df = load_data()

if not df.empty:
    search = st.sidebar.text_input("🔍 Search")
    # Filtering logic
    filtered_df = df[df['Headline'].str.contains(search, case=False)] if search else df
    
    st.write(f"Showing {len(filtered_df)} signals")
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No data found. Wait for the first GitHub Action to run.")
