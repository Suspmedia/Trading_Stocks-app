# tabs/tab1_india_stocks.py

import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt
from datetime import datetime, timedelta

def show():
    st.header("📈 Indian Stock Analyzer")

    # Predefined F&O stock list with key additions
    predefined_stocks = sorted([
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
    ])

    selected_stock = st.selectbox("🔍 Select a stock", predefined_stocks)

    # Timeframe selector
    timeframe = st.selectbox("🕒 Select timeframe", ["5 days", "14 days", "21 days"])
    days_map = {"5 days": 5, "14 days": 14, "21 days": 21}
    num_days = days_map[timeframe]

    end_date = datetime.today()
    start_date = end_date - timedelta(days=num_days * 2)

    # Load stock data
    try:
        df = yf.download(selected_stock, start=start_date, end=end_date, progress=False)
        df.reset_index(inplace=True)
        df = df[['Date', 'Open', 'High', 'Low', 'Close']]
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.tail(num_days)
        source = df.copy()
    except Exception as e:
        st.warning("⚠️ Failed to fetch stock data.")
        return

    st.subheader(f"{selected_stock.replace('.NS','')} OHLC Chart (Altair)")

    base = alt.Chart(source).encode(x='Date:T')

    rule = base.mark_rule().encode(
        y='Low:Q',
        y2='High:Q',
        color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red"))
    )

    bar = base.mark_bar().encode(
        y=alt.Y('Open:Q', title="Price"),
        y2='Close:Q',
        color=alt.condition("datum.Open <= datum.Close", alt.value("green"), alt.value("red"))
    )

    ohlc_chart = (rule + bar).properties(width=800, height=400)
    st.altair_chart(ohlc_chart, use_container_width=True)

    # Show Data Table
    with st.expander("📋 View OHLC Data"):
        st.dataframe(df.set_index("Date"))

