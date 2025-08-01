import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import io

@st.cache_data
def load_default_stock_list():
    return [
        'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BHARTIARTL.NS',
        'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS',
        'HCLTECH.NS', 'HDFCBANK.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INFY.NS',
        'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS',
        'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
        'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'ULTRACEMCO.NS',
        'WIPRO.NS', 'INDIANB.NS', 'YESBANK.NS', 'BANKBARODA.NS', 'CANBK.NS', 'UNIONBANK.NS',
        'PNB.NS', 'FEDERALBNK.NS'
    ]

def fetch_yfinance_data(symbols):
    try:
        data = yf.download(tickers=" ".join(symbols), period="2d", interval="1d", group_by='ticker', progress=False)
        records = []
        for symbol in symbols:
            if symbol in data:
                df = data[symbol].copy()
                if len(df) >= 2:
                    prev_close = df.iloc[-2]['Close']
                    today_close = df.iloc[-1]['Close']
                    change_pct = ((today_close - prev_close) / prev_close) * 100
                    records.append({
                        'Symbol': symbol.replace('.NS', ''),
                        'Previous Close': round(prev_close, 2),
                        'Close': round(today_close, 2),
                        'Change %': round(change_pct, 2),
                        'Volume': int(df.iloc[-1]['Volume'])
                    })
        return pd.DataFrame(records).sort_values(by='Change %', ascending=False)
    except Exception as e:
        st.error(f"Error fetching live data: {e}")
        return pd.DataFrame()

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def tab2_summary_report():
    st.header("📋 Daily Summary Report")

    # Step 1: Choose source
    use_uploaded = st.toggle("📂 Upload Full NSE Equity List (optional)")
    default_symbols = load_default_stock_list()
    stock_df = pd.DataFrame(default_symbols, columns=['Symbol'])

    if use_uploaded:
        uploaded_file = st.file_uploader("Upload your CSV (must contain 'Symbol' column)", type=["csv"])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Symbol' in df.columns:
                    stock_df = df[['Symbol']].dropna()
                else:
                    st.warning("Uploaded CSV must have a 'Symbol' column.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    symbols = [s if s.endswith('.NS') else f"{s}.NS" for s in stock_df['Symbol'].tolist()]

    # Step 2: Fetch data
    st.info("📡 Fetching live data from Yahoo Finance...")
    summary_df = fetch_yfinance_data(symbols)

    if summary_df.empty:
        st.warning("⚠️ No data available.")
        return

    # Add RSI
    rsi_data = []
    for symbol in symbols:
        try:
            df = yf.download(symbol, period="30d", interval="1d", progress=False)
            if not df.empty:
                rsi_val = calculate_rsi(df['Close']).iloc[-1]
                rsi_data.append({'Symbol': symbol.replace('.NS', ''), 'RSI': round(rsi_val, 2)})
        except:
            rsi_data.append({'Symbol': symbol.replace('.NS', ''), 'RSI': None})

    rsi_df = pd.DataFrame(rsi_data)
    summary_df = pd.merge(summary_df, rsi_df, on='Symbol', how='left')

    # Tabs
    tabs = st.tabs(["📈 Gainers", "📉 Losers", "🔼 Most Active", "📊 RSI Signals", "⬆️ Breakout Watch"])

    with tabs[0]:
        st.subheader("Top 50 Gainers")
        st.dataframe(summary_df.sort_values(by="Change %", ascending=False).head(50))

    with tabs[1]:
        st.subheader("Top 50 Losers")
        st.dataframe(summary_df.sort_values(by="Change %", ascending=True).head(50))

    with tabs[2]:
        st.subheader("Top 50 by Volume")
        st.dataframe(summary_df.sort_values(by="Volume", ascending=False).head(50))

    with tabs[3]:
        st.subheader("Stocks with RSI < 30 (Possible Oversold)")
        st.dataframe(summary_df[summary_df['RSI'] < 30].sort_values(by="RSI").head(50))

    with tabs[4]:
        st.subheader("Breakout Watch (RSI > 70 & Gaining)")
        st.dataframe(summary_df[(summary_df['RSI'] > 70) & (summary_df['Change %'] > 0)].sort_values(by="Change %", ascending=False).head(50))
