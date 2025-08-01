import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
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
    st.header("📈 Indian Stock Charts")

    all_stocks = get_nse_stock_list()

    col1, col2 = st.columns([1, 3])
    with col1:
        selected_letter = st.selectbox("Filter by alphabet", ['All'] + list(string.ascii_uppercase))
    if selected_letter == 'All':
        filtered_stocks = all_stocks
    else:
        filtered_stocks = {k: v for k, v in all_stocks.items() if k.startswith(selected_letter)}

    with col2:
        selected_stock_name = st.selectbox("Select a stock", list(filtered_stocks.keys()))

    selected_symbol = filtered_stocks[selected_stock_name]

    timeframe = st.selectbox("Select timeframe", ["5d", "14d", "21d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=5)
    interval = st.selectbox("Select interval", ["1d", "1wk", "1mo"], index=0)

    try:
        data = yf.download(selected_symbol, period=timeframe, interval=interval, progress=False)
        data.dropna(inplace=True)
        if data.shape[0] < 5:
            st.warning("⚠️ Not enough data to show a meaningful chart. Try a longer timeframe.")
            return

        st.subheader(f"{selected_stock_name} ({selected_symbol})")
        with st.expander("📄 View Raw OHLC Data"):
            st.dataframe(data.tail(50))

        # Altair OHLC Chart
        df = data.reset_index()
        df['Date'] = pd.to_datetime(df['Date'])
        base = alt.Chart(df).encode(x='Date:T')
        rule = base.mark_rule().encode(
            y='Low:Q',
            y2='High:Q'
        )
        bar = base.mark_bar().encode(
            y='Open:Q',
            y2='Close:Q',
            color=alt.condition("datum.Open <= datum.Close",
                                alt.value("#00b300"),  # Green
                                alt.value("#e60000"))  # Red
        )
        ohlc_chart = (rule + bar).properties(
            width=1000,
            height=500,
            title=f"{selected_stock_name} OHLC Chart (Altair)"
        )
        st.altair_chart(ohlc_chart, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading chart: {e}")
