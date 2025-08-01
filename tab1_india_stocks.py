import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def run():
    st.header("📊 Indian Stock Market Analysis")
    stock = st.text_input("Enter Stock Symbol (e.g., INFY.NS)", "INFY.NS")
    data = yf.download(stock, period="1mo", interval="1d")
    if not data.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        )])
        st.plotly_chart(fig, use_container_width=True)
