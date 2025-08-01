# tab2_summary_report.py

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

@st.cache_data(ttl=3600)
def fetch_data(symbols):
    all_data = []
    for symbol in symbols:
        try:
            df = yf.download(symbol + ".NS", period="2d", interval="1d", progress=False)
            if len(df) < 2:
                continue
            close_today = df["Close"].iloc[-1]
            close_yesterday = df["Close"].iloc[-2]
            pct_change = ((close_today - close_yesterday) / close_yesterday) * 100
            volume = df["Volume"].iloc[-1]
            all_data.append({
                "Symbol": symbol,
                "Close": close_today,
                "% Change": round(pct_change, 2),
                "Volume": volume,
            })
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
    return pd.DataFrame(all_data)

def show():
    st.subheader("📅 Daily Summary Report")

    # Choose stock universe
    mode = st.radio("Select Mode", ["NIFTY 500", "Manual CSV Upload (Full NSE)"])

    if mode == "NIFTY 500":
        nifty_500 = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty500list.csv")
        symbols = nifty_500["Symbol"].unique().tolist()
    else:
        uploaded_file = st.file_uploader("Upload NSE Stock List CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                user_df = pd.read_csv(uploaded_file)
                symbols = user_df["Symbol"].unique().tolist()
            except Exception as e:
                st.error(f"Failed to read uploaded CSV: {e}")
                return
        else:
            st.warning("Please upload a CSV file.")
            return

    if not symbols:
        st.warning("No symbols available.")
        return

    with st.spinner("Fetching live data..."):
        data = fetch_data(symbols)

    if data.empty or not set(["% Change", "Close", "Volume"]).issubset(data.columns):
        st.error("Data fetch failed or missing required columns.")
        return

    data = data.dropna(subset=["% Change", "Close", "Volume"])  # Clean rows with missing values

    # Sorting tabs
    tabs = st.tabs(["🔼 Top 50 Gainers", "🔽 Top 50 Losers", "📊 Top by Volume", "📈 RSI Candidates"])

    with tabs[0]:
        gainers = data.sort_values(by="% Change", ascending=False).head(50).reset_index(drop=True)
        st.dataframe(gainers)

    with tabs[1]:
        losers = data.sort_values(by="% Change", ascending=True).head(50).reset_index(drop=True)
        st.dataframe(losers)

    with tabs[2]:
        top_vol = data.sort_values(by="Volume", ascending=False).head(50).reset_index(drop=True)
        st.dataframe(top_vol)

    with tabs[3]:
        # Simulated RSI candidates (mock logic for now)
        rsi_candidates = data[
            (data["% Change"] < -2) & (data["Volume"] > data["Volume"].median())
        ].sort_values(by="% Change").head(50).reset_index(drop=True)
        st.dataframe(rsi_candidates)
