import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime

@st.cache_data
def fetch_from_nse_html():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        session = requests.Session()
        url = "https://www.nseindia.com/market-data/top-gainers-loosers"
        response = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table")

        gainers_df = pd.read_html(str(tables[0]))[0] if tables else pd.DataFrame()
        losers_df = pd.read_html(str(tables[1]))[0] if len(tables) > 1 else pd.DataFrame()
        return gainers_df, losers_df
    except:
        return None, None

@st.cache_data
def fetch_from_nse_csv():
    date_str = datetime.now().strftime("%d%m%Y")
    base_url = "https://www1.nseindia.com/content/nsccl/"
    try:
        gainers_url = f"{base_url}niftyGainers_{date_str}.csv"
        losers_url = f"{base_url}niftyLosers_{date_str}.csv"
        gainers_df = pd.read_csv(gainers_url)
        losers_df = pd.read_csv(losers_url)
        return gainers_df, losers_df
    except:
        return None, None

@st.cache_data
def fetch_all_nse_stocks():
    try:
        url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        records = data["data"]
        df = pd.DataFrame(records)
        return df
    except:
        return None

@st.cache_data
def fetch_from_yfinance():
    try:
        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period="2d", interval="1d").reset_index()
        if len(hist) < 2:
            return None, None
        change = hist.iloc[1]['Close'] - hist.iloc[0]['Close']
        percent_change = (change / hist.iloc[0]['Close']) * 100
        df = pd.DataFrame([{
            "Stock": "NIFTY 50",
            "Previous Close": hist.iloc[0]['Close'],
            "Current Close": hist.iloc[1]['Close'],
            "Change": round(change, 2),
            "Percent Change": f"{percent_change:.2f}%"
        }])
        return df, df
    except:
        return None, None

def run():
    st.header("📅 Daily Summary Report (Post-Market)")

    source = st.selectbox("Select Data Source", ["From NSE HTML", "From NSE CSV", "From Yahoo Finance"])

    gainers, losers = None, None
    all_stocks = None

    if source == "From NSE HTML":
        gainers, losers = fetch_from_nse_html()
        all_stocks = fetch_all_nse_stocks()
    elif source == "From NSE CSV":
        gainers, losers = fetch_from_nse_csv()
        all_stocks = fetch_all_nse_stocks()
    elif source == "From Yahoo Finance":
        gainers, losers = fetch_from_yfinance()

    tab_titles = ["📈 Top Gainers", "📉 Top Losers"]
    if all_stocks is not None and not all_stocks.empty:
        tab_titles.append("📊 All Stocks (Nifty 500)")

    tabs = st.tabs(tab_titles)

    if gainers is not None and not gainers.empty:
        with tabs[0]:
            st.dataframe(gainers, use_container_width=True)
    else:
        with tabs[0]:
            st.warning("Top gainers data not available.")

    if losers is not None and not losers.empty:
        with tabs[1]:
            st.dataframe(losers, use_container_width=True)
    else:
        with tabs[1]:
            st.warning("Top losers data not available.")

    if all_stocks is not None and not all_stocks.empty and len(tabs) > 2:
        with tabs[2]:
            st.dataframe(all_stocks, use_container_width=True)
