# tab2_summary_report.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# List of NIFTY 100 symbols
NIFTY100_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ITC.NS", "LT.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "BAJFINANCE.NS",
    "ASIANPAINT.NS", "HCLTECH.NS", "AXISBANK.NS", "MARUTI.NS", "SUNPHARMA.NS", "NTPC.NS",
    "ULTRACEMCO.NS", "NESTLEIND.NS", "TITAN.NS", "POWERGRID.NS", "WIPRO.NS", "TECHM.NS",
    "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "BAJAJFINSV.NS", "BRITANNIA.NS",
    "COALINDIA.NS", "DIVISLAB.NS", "GRASIM.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HDFCLIFE.NS", "IOC.NS", "JSWSTEEL.NS", "M&M.NS", "ONGC.NS", "SHREECEM.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "UPL.NS", "BAJAJ-AUTO.NS", "BPCL.NS", "CIPLA.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "INDUSINDBK.NS", "SBILIFE.NS", "SIEMENS.NS", "PIDILITIND.NS",
    "DABUR.NS", "GAIL.NS", "HAVELLS.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IGL.NS", "INDIGO.NS",
    "MARICO.NS", "MUTHOOTFIN.NS", "NAUKRI.NS", "PEL.NS", "SRF.NS", "TATACONSUM.NS",
    "TORNTPHARM.NS", "VEDL.NS", "ZOMATO.NS", "DMART.NS", "LTIM.NS", "TVSMOTOR.NS"
]

# Helper functions
@st.cache_data(ttl=3600)
def fetch_data(symbols):
    data = []
    end = datetime.now()
    start = end - timedelta(days=5)

    df = yf.download(symbols, start=start, end=end, interval="1d", group_by="ticker", progress=False, threads=True)

    for symbol in symbols:
        try:
            d = df[symbol].copy()
            d["Symbol"] = symbol
            d["% Change"] = d["Close"].pct_change() * 100
            d["RSI"] = calculate_rsi(d["Close"])
            d["SMA_5"] = d["Close"].rolling(window=5).mean()
            last_row = d.iloc[-1]
            info = yf.Ticker(symbol).info
            data.append({
                "Symbol": symbol,
                "Close": last_row["Close"],
                "% Change": last_row["% Change"],
                "Volume": last_row["Volume"],
                "RSI": last_row["RSI"],
                "SMA_5": last_row["SMA_5"],
                "P/E Ratio": info.get("trailingPE", np.nan)
            })
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue

    return pd.DataFrame(data)

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

# UI
def show():
    st.header("📅 Daily Summary Report (NIFTY 100 Only)")

    data_load_state = st.info("Loading data for NIFTY 100 stocks...")
    df = fetch_data(NIFTY100_SYMBOLS)
    data_load_state.empty()

    if df.empty:
        st.warning("No data available.")
        return

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    rsi_min = st.sidebar.slider("Minimum RSI", 0, 100, 30)
    rsi_max = st.sidebar.slider("Maximum RSI", 0, 100, 70)
    pe_max = st.sidebar.number_input("Max P/E Ratio", value=40.0, step=1.0)

    filtered = df[
        (df["RSI"].between(rsi_min, rsi_max)) &
        (df["P/E Ratio"] < pe_max)
    ]

    tab1, tab2, tab3 = st.tabs(["📈 Top Gainers", "📉 Top Losers", "🔥 Volume Leaders"])

    with tab1:
        st.subheader("📈 Top 50 Gainers")
        gainers = filtered.sort_values(by="% Change", ascending=False).head(50)
        st.dataframe(gainers, use_container_width=True)

    with tab2:
        st.subheader("📉 Top 50 Losers")
        losers = filtered.sort_values(by="% Change", ascending=True).head(50)
        st.dataframe(losers, use_container_width=True)

    with tab3:
        st.subheader("🔥 Top 50 by Volume")
        top_volume = filtered.sort_values(by="Volume", ascending=False).head(50)
        st.dataframe(top_volume, use_container_width=True)

    # Export
    csv = convert_df(filtered)
    st.download_button(
        "📤 Download Filtered Data as CSV",
        data=csv,
        file_name="nifty100_summary_filtered.csv",
        mime="text/csv"
    )
