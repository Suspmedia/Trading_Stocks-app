import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

# Fixed stock list (add more if needed)
stock_list = [
    "ASIANPAINT.NS", "TCS.NS", "RELIANCE.NS", "INFY.NS", "ICICIBANK.NS",
    "HDFCBANK.NS", "SBIN.NS", "AXISBANK.NS", "YESBANK.NS", "INDIANB.NS"
]

# Mapping to show clean names
stock_name_map = {s: s.replace(".NS", "") for s in stock_list}

st.header("📈 Indian Stock Viewer")

# Timeframe selection
timeframe = st.selectbox("Select Timeframe", ["5 Day", "14 Day", "21 Day"])
days_map = {"5 Day": 5, "14 Day": 14, "21 Day": 21}
days = days_map[timeframe]

# Stock selection
selected_stock = st.selectbox("Select Stock", stock_list)
selected_stock_name = stock_name_map[selected_stock]

# Toggle for chart view
show_full_range = st.checkbox("Show full OHLC range (include wicks)", value=False)

# Fetch data
@st.cache_data(ttl=3600)
def fetch_data(ticker, period_days):
    end = datetime.now()
    start = end - timedelta(days=period_days + 2)
    df = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), interval='1d')
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    return df.tail(period_days)

df = fetch_data(selected_stock, days)

if df.empty:
    st.warning("No data found for this stock and timeframe.")
else:
    st.dataframe(df[['Date', 'Open', 'High', 'Low', 'Close']], use_container_width=True)

    st.subheader(f"{selected_stock_name} OHLC Chart (Altair)")

    # Set y-axis scale
    if show_full_range:
        y_scale = alt.Scale(domain=[df['Low'].min() - 10, df['High'].max() + 10])
    else:
        body_min = df[['Open', 'Close']].min().min()
        body_max = df[['Open', 'Close']].max().max()
        y_scale = alt.Scale(domain=[body_min - 10, body_max + 10])

    base = alt.Chart(df).encode(x=alt.X('Date:T', title='Date'))

    # Wicks (High-Low)
    wick = base.mark_rule().encode(
        y=alt.Y('Low:Q', scale=y_scale, title='Price'),
        y2='High:Q'
    )

    # Candle bodies (Open-Close)
    candle = base.mark_bar().encode(
        y='Open:Q',
        y2='Close:Q',
        color=alt.condition("datum.Open <= datum.Close",
                            alt.value("#00b300"),  # green
                            alt.value("#e60000"))  # red
    )

    chart = (wick + candle).properties(width=1000, height=500)
    st.altair_chart(chart, use_container_width=True)
