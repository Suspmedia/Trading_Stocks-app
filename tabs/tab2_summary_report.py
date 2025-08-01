import streamlit as st
import pandas as pd
import requests

def fetch_nse_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data['data'])
        else:
            st.error("Failed to fetch data.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

def run():
    st.header("📅 Daily Market Summary (NSE - Post Market)")

    tabs = st.tabs(["Top Gainers", "Top Losers", "Most Active"])

    with tabs[0]:
        st.subheader("📈 Top Gainers")
        url_gainers = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
        gainers = fetch_nse_data(url_gainers)
        if not gainers.empty:
            st.dataframe(gainers[["symbol", "lastPrice", "pChange", "previousClose"]])

    with tabs[1]:
        st.subheader("📉 Top Losers")
        url_losers = "https://www.nseindia.com/api/live-analysis-variations?index=losers"
        losers = fetch_nse_data(url_losers)
        if not losers.empty:
            st.dataframe(losers[["symbol", "lastPrice", "pChange", "previousClose"]])

    with tabs[2]:
        st.subheader("🔥 Most Active by Volume")
        url_volume = "https://www.nseindia.com/api/live-analysis-most-active?index=volume"
        active = fetch_nse_data(url_volume)
        if not active.empty:
            st.dataframe(active[["symbol", "lastPrice", "tradedQuantity", "turnoverInLakhs"]])
