import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def load_eod_summary():
    """Fetch EOD top gainers and losers CSVs from NSE"""
    date_str = datetime.now().strftime("%d%m%Y")
    base_url = "https://www1.nseindia.com/content/nsccl/"
    
    try:
        gainers_url = f"{base_url}niftyGainers_{date_str}.csv"
        losers_url = f"{base_url}niftyLosers_{date_str}.csv"

        gainers_df = pd.read_csv(gainers_url)
        losers_df = pd.read_csv(losers_url)

        return gainers_df, losers_df
    except Exception as e:
        return None, None

def run():
    st.header("📅 Daily Summary Report (Post-Market)")

    gainers_df, losers_df = load_eod_summary()

    if gainers_df is not None and losers_df is not None:
        tabs = st.tabs(["Top Gainers", "Top Losers"])

        with tabs[0]:
            st.subheader("📈 Top Gainers Today")
            st.dataframe(gainers_df, use_container_width=True)

        with tabs[1]:
            st.subheader("📉 Top Losers Today")
            st.dataframe(losers_df, use_container_width=True)
    else:
        st.error("⚠️ Failed to fetch EOD data from NSE. Please try again later.")
