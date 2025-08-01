import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Static NSE stock list (your preferred list)
def get_nse_stock_list():
    return {
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

def show():
    st.header("📈 Indian Stock Line Chart with Volume")

    stock_dict = get_nse_stock_list()
    selected_stock = st.selectbox("Select a Stock", list(stock_dict.keys()))
    symbol = stock_dict[selected_stock]

    timeframe_options = {
        "1 Hour": ("2d", "1h"),
        "1 Day": ("5d", "1d"),
        "1 Week": ("1mo", "1d"),
        "1 Month": ("3mo", "1d")
    }

    timeframe_label = st.selectbox("Select Timeframe", list(timeframe_options.keys()))
    period, interval = timeframe_options[timeframe_label]

    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if df.empty:
            st.warning("⚠️ No data found.")
            return

        df.dropna(inplace=True)

        fig = go.Figure()

        # Line chart for Close price
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='deepskyblue')
        ))

        # Volume as bar chart
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'],
            name='Volume',
            yaxis='y2',
            marker=dict(color='lightgray'),
            opacity=0.4
        ))

        # Layout settings
        fig.update_layout(
            title=f"{selected_stock} - Line Chart with Volume",
            xaxis_title='Date',
            yaxis_title='Price (INR)',
            yaxis2=dict(
                title='Volume',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            template='plotly_white',
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
