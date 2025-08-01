# tabs/tab1_india_stocks.py

import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

def show():
    st.header("📈 Indian Stock Analyzer")

    # Your exact custom stock list
    stock_dict = {
        'ASIANPAINT': 'ASIANPAINT.NS', 'AXISBANK': 'AXISBANK.NS', 'BAJAJ-AUTO': 'BAJAJ-AUTO.NS',
        'BAJFINANCE': 'BAJFINANCE.NS', 'BHARTIARTL': 'BHARTIARTL.NS', 'CIPLA': 'CIPLA.NS',
        'COALINDIA': 'COALINDIA.NS', 'DIVISLAB': 'DIVISLAB.NS', 'DRREDDY': 'DRREDDY.NS',
        'EICHERMOT': 'EICHERMOT.NS', 'GRASIM': 'GRASIM.NS', 'HCLTECH': 'HCLTECH.NS',
        'HDFCBANK': 'HDFCBANK.NS', 'HINDALCO': 'HINDALCO.NS', 'HINDUNILVR': 'HINDUNILVR.NS',
        'ICICIBANK': 'ICICIBANK.NS', 'INFY': 'INFY.NS', 'ITC': 'ITC.NS', 'JSWSTEEL': 'JSWSTEEL.NS',
        'KOTAKBANK': 'KOTAKBANK.NS', 'LT': 'LT.NS', 'M&M': 'M&M.NS', 'MARUTI': 'MARUTI.NS',
        'NESTLEIND': 'NESTLEIND.NS', 'NTPC': 'NTPC.NS', 'ONGC': 'ONGC.NS', 'POWERGRID': 'POWERGRID.NS',
        'RELIANCE': 'RELIANCE.NS', 'SBIN': 'SBIN.NS', 'SUNPHARMA': 'SUNPHARMA.NS',
        'TATAMOTORS': 'TATAMOTORS.NS', 'TATASTEEL': 'TATASTEEL.NS', 'TCS': 'TCS.NS',
        'TECHM': 'TECHM.NS', 'TITAN': 'TITAN.NS', 'ULTRACEMCO': 'ULTRACEMCO.NS', 'WIPRO': 'WIPRO.NS',
        'INDIANB': 'INDIANB.NS', 'YESBANK': 'YESBANK.NS', 'BANKBARODA': 'BANKBARODA.NS',
        'CANBK': 'CANBK.NS', 'UNIONBANK': 'UNIONBANK.NS', 'PNB': 'PNB.NS', 'FEDERALBNK': 'FEDERALBNK.NS',
    }

    stock_names = list(stock_dict.keys())
    selected_name = st.selectbox("🔍 Select a stock", stock_names)
    selected_stock = stock_dict[selected_name]

    # Timeframe selector
    timeframe = st.selectbox("🕒 Select timeframe", ["5 days", "14 days", "21 days"])
    num_days = {"5 days": 5, "14 days": 14, "21 days": 21}[timeframe]

    end_date = datetime.today()
    start_date = end_date - timedelta(days=num_days * 2)

    try:
        df = yf.download(selected_stock, start=start_date, end=end_date, progress=False)
        df.reset_index(inplace=True)
        df = df[['Date', 'Open', 'High', 'Low', 'Close']]
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.tail(num_days)
        source = df.copy()
    except Exception as e:
        st.warning(f"⚠️ Failed to fetch data for {selected_stock}")
        return

    st.subheader(f"{selected_name} ({selected_stock}) OHLC Chart")

    base = alt.Chart(source).encode(x='Date:T')

    rule = base.mark_rule().encode(
        y='Low:Q',
        y2='High:Q',
        color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red"))
    )

    bar = base.mark_bar().encode(
        y='Open:Q',
        y2='Close:Q',
        color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red"))
    )

    ohlc_chart = (rule + bar).properties(width=800, height=400)
    st.altair_chart(ohlc_chart, use_container_width=True)

    with st.expander("📋 View OHLC Data"):
        st.dataframe(df.set_index("Date"))
