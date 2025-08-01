import streamlit as st
import yfinance as yf
import pandas as pd
import string

@st.cache_data
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
    st.header("📄 Indian Stock OHLC Data Viewer")

    all_stocks = get_nse_stock_list()

    # Stock filter
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_letter = st.selectbox("Filter by alphabet", ['All'] + list(string.ascii_uppercase))

    filtered_stocks = all_stocks if selected_letter == 'All' else {
        k: v for k, v in all_stocks.items() if k.startswith(selected_letter)
    }

    with col2:
        selected_stock_name = st.selectbox("Select stock", list(filtered_stocks.keys()))

    selected_symbol = filtered_stocks[selected_stock_name]

    # Timeframe and interval
    timeframe = st.selectbox("Select timeframe", ["5d", "14d", "21d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
    interval = st.selectbox("Select interval", ["1h", "1d", "1wk", "1mo"])

    # Optional indicators
    show_sma = st.checkbox("Show SMA (Simple Moving Average)", value=True)
    show_volume = st.checkbox("Show Volume", value=True)
    show_rsi = st.checkbox("Show RSI", value=False)

    try:
        df = yf.download(selected_symbol, period=timeframe, interval=interval, progress=False)

        if df.empty:
            st.warning("⚠️ No data found.")
            return

        if show_sma:
            df["SMA_10"] = df["Close"].rolling(window=10).mean()
        if show_rsi:
            delta = df["Close"].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            df["RSI"] = 100 - (100 / (1 + rs))

        st.subheader(f"{selected_stock_name} ({selected_symbol}) OHLC Data")
        st.dataframe(df.tail(100))

        # Export option
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{selected_symbol}_{interval}.csv",
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Error fetching data: {e}")
