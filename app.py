import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Atlas Agentic Intelligence")

# --- DATA LOADING ---
DATA_PATH = "data/research_data.csv"

@st.cache_data(ttl=3600) # Cache for 1 hour to keep it fast
def load_atlas_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        st.error(f"⚠️ Intel file not found at {DATA_PATH}. Ensure your Scraper has run at least once.")
        return pd.DataFrame()

df = load_atlas_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Atlas Intel Filters")

if not df.empty:
    # Date Range Filter
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Timeframe",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Region Filter
    regions = st.sidebar.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
    
    # Visualization Type
    chart_type = st.sidebar.selectbox("View Mode", ["News Feed", "Regional Analysis", "Source Breakdown"])

    # --- MAIN CONTENT ---
    st.title("🔬 Atlas Agentic: Real-Time Biotech Intel")
    
    # Filter the Dataframe based on sidebar
    if len(date_range) == 2:
        start, end = date_range
        mask = (df['Date'].dt.date >= start) & (df['Date'].dt.date <= end) & (df['Region'].isin(regions))
        filtered_df = df.loc[mask]
    else:
        filtered_df = df

    # Display Content
    if chart_type == "News Feed":
        st.subheader("Latest Global & LMIC Signals")
        # Display as a clean list of clickable headlines
        for i, row in filtered_df.iterrows():
            st.markdown(f"**[{row['Source']}]** {row['Headline']}  \n[Read Source Article]({row['Link']})")
            st.divider()

    elif chart_type == "Regional Analysis":
        st.subheader("Intel Volume by Region")
        fig = px.pie(filtered_df, names="Region", color_discrete_sequence=['#1DE9B6', '#263238'])
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Source Breakdown":
        st.subheader("Intelligence Volume by Source")
        fig = px.bar(filtered_df, x="Source", color="Region", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    # Footer/Meta Info
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Last Intelligence Sync: {df['Date'].max().strftime('%Y-%m-%d')}")


