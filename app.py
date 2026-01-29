import streamlit as st
import pandas as pd

# Basic Page Setup
st.set_page_config(page_title="Biotech Intelligence Portal", page_icon="🔬")

st.title("🔬 LMIC Biotech Research Feed")
st.subheader("Automated Intelligence for Karl Kaddu")

# Mock data to simulate your Python Scraper output
data = {
    'Date': ['2026-01-02', '2026-01-04', '2026-01-05'],
    'Source': ['SAMRC South Africa', 'Fiocruz Brazil', 'PIB India'],
    'Breakthrough': [
        'Modular mRNA TB vaccine trials enter Phase II.',
        'New CRISPR diagnostic kit for Dengue costed at $1.50.',
        'Biofoundry network launches in Hyderabad.'
    ]
}
df = pd.DataFrame(data)

search = st.text_input("Search breakthroughs (e.g., 'mRNA'):")
if search:
    df = df[df['Breakthrough'].str.contains(search, case=False)]

st.table(df)

st.info("💡 This is a live preview of my 'Technical Translator' automation engine.")

