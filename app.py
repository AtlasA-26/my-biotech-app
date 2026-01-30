import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide", page_title="Atlas Agentic Intelligence")

# --- DATA LOADING ---
DATA_PATH = "data/research_data.csv"

@st.cache_data(ttl=3600)
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
    # 1. KEYWORD SEARCH (The New Feature)
    search_query = st.sidebar.text_input("🔍 Search Intelligence", placeholder="e.g. Vaccine, Policy, Nigeria...")

    # 2. DATE RANGE
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input("Select Timeframe", value=(min_date, max_date))

    # 3. REGION SELECT
    regions = st.sidebar.multiselect("Select Regions", options=df['Region'].unique(), default=df['Region'].unique())
    
    chart_type = st.sidebar.selectbox("View Mode", ["News Feed", "Analytics Dashboard"])

    # --- DATA FILTERING LOGIC ---
    mask = (df['Region'].isin(regions))
    
    if len(date_range) == 2:
        start, end = date_range
        mask = mask & (df['Date'].dt.date >= start) & (df['Date'].dt.date <= end)
    
    # Apply Keyword Search
    if search_query:
        mask = mask & (df['Headline'].str.contains(search_query, case=False, na=False))

    filtered_df = df.loc[mask]

    # --- MAIN CONTENT ---
    st.title("🔬 Atlas Agentic Intelligence")
    
    # Action Bar: Results count and Download button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"Showing **{len(filtered_df)}** signals found.")
    with col2:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Results", data=csv, file_name="atlas_export.csv", mime="text/csv")

    if chart_type == "News Feed":
        if not filtered_df.empty:
            for _, row in filtered_df.sort_values(by="Date", ascending=False).iterrows():
                with st.container():
                    st.markdown(f"**{row['Date'].strftime('%Y-%m-%d')}** | **{row['Source']}**")
                    st.markdown(f"#### {row['Headline']}")
                    st.markdown(f"[🔗 View Original Source]({row['Link']})")
                    st.divider()
        else:
            st.warning("No signals match your search criteria.")

    elif chart_type == "Analytics Dashboard":
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Regional Distribution")
            st.plotly_chart(px.pie(filtered_df, names="Region", hole=0.4), use_container_width=True)
        with c2:
            st.subheader("Source Volume")
            st.plotly_chart(px.bar(filtered_df, x="Source", color="Source"), use_container_width=True)

    st.sidebar.caption(f"Last Sync: {df['Date'].max().strftime('%Y-%m-%d')}")



