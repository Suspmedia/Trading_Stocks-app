# tab2_summary_report.py

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# List of NIFTY 100 stock symbols
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

# Fetch stock data
@st.cache_data(ttl=3600)
def fetch_data(symbols):
    end = datetime.now()
    start = end - timedelta(days=5)
    df = yf.download(symbols, start=start, end=end, interval="1d", group_by="ticker", progress=False, threads=True)

    data = []
    for symbol in symbols:
        try:
            d = df[symbol].copy()
            d["Symbol"] = symbol
            d["% Change"] = d["Close"].pct_change() * 100
            d["RSI"] = calculate_rsi(d["Close"])
            d["SMA_5"] = d["Close"].rolling(window=5).mean()
            last = d.iloc[-1]
            data.append({
                "Symbol": symbol,
                "Close": round(last["Close"], 2),
                "% Change": round(last["% Change"], 2),
                "Volume": int(last["Volume"]),
                "RSI": round(last["RSI"], 2),
                "SMA_5": round(last["SMA_5"], 2)
            })
        except Exception as e:
            print(f"Error for {symbol}: {e}")
            continue

    return pd.DataFrame(data)

# Calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# Main UI
def show():
    st.header("📊 Daily Summary Report (NIFTY 100 Only)")

    with st.spinner("Fetching latest data..."):
        df = fetch_data(NIFTY100_SYMBOLS)

    if df.empty:
        st.warning("⚠️ No data available.")
        return

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Top Gainers", "Top Losers", "Top by Volume"])

    with tab1:
        st.subheader("📈 Top 50 Gainers")
        gainers = df.sort_values(by="% Change", ascending=False).head(50)
        st.dataframe(gainers, use_container_width=True)

    with tab2:
        st.subheader("📉 Top 50 Losers")
        losers = df.sort_values(by="% Change", ascending=True).head(50)
        st.dataframe(losers, use_container_width=True)

    with tab3:
        st.subheader("🔥 Top 50 by Volume")
        top_vol = df.sort_values(by="Volume", ascending=False).head(50)
        st.dataframe(top_vol, use_container_width=True)

    # Export
    csv = convert_df(df)
    st.download_button(
        "📤 Download Full Summary as CSV",
        data=csv,
        file_name="nifty100_summary.csv",
        mime="text/csv"
    )
