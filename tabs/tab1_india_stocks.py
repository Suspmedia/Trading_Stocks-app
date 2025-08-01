import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# Helper to fetch stock list
def get_nse_stock_list():
    # Common NSE stock tickers with Yahoo-compatible symbols
    return {
        'RELIANCE': 'RELIANCE.NS',
        'TCS': 'TCS.NS',
        'INFY': 'INFY.NS',
        'ICICIBANK': 'ICICIBANK.NS',
        'HDFCBANK': 'HDFCBANK.NS',
        'SBIN': 'SBIN.NS',
        'LT': 'LT.NS',
        'MARUTI': 'MARUTI.NS',
        'AXISBANK': 'AXISBANK.NS',
        'HINDUNILVR': 'HINDUNILVR.NS',
        'ITC': 'ITC.NS',
        'BAJFINANCE': 'BAJFINANCE.NS',
        'WIPRO': 'WIPRO.NS'
    }

# Main display function
def show_stock_charts():
    st.header("📈 NSE India Stock Charts")

    stocks = get_nse_stock_list()
    selected_stock_name = st.selectbox("Choose a stock", list(stocks.keys()))
    selected_symbol = stocks[selected_stock_name]

    # Select timeframe
    timeframe = st.selectbox("Timeframe", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
    interval = st.selectbox("Interval", ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"])

    # Fetch data
    try:
        data = yf.download(selected_symbol, period=timeframe, interval=interval, progress=False)
        if data.empty:
            st.warning("No data available for the selected options.")
            return

        # Show raw data
        with st.expander("📄 View Raw Data"):
            st.dataframe(data.tail(50))

        # Plot candlestick chart
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlesticks'))

        fig.update_layout(
            title=f"{selected_stock_name} ({selected_symbol}) Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Failed to load stock data: {e}")
