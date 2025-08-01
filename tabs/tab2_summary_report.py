import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

def load_nse_bhavcopy_data():
    today = datetime.date.today()
    filename = f"cm{today.strftime('%d%b%Y').upper()}bhav.csv"
    url = f"https://www1.nseindia.com/content/historical/EQUITIES/{today.strftime('%Y')}/{today.strftime('%b').upper()}/{filename}.zip"
    try:
        df = pd.read_csv(url, compression='zip')
        df = df[df['SERIES'] == 'EQ']
        df = df[['SYMBOL', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'PREVCLOSE', 'TOTTRDQTY', 'TOTTRDVAL']]
        df["PERCENT_CHANGE"] = ((df["CLOSE"] - df["PREVCLOSE"]) / df["PREVCLOSE"]) * 100
        return df
    except:
        return None

def load_from_yfinance():
    try:
        nifty_stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']  # Example: you can expand this list
        data = []
        for ticker in nifty_stocks:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if len(hist) >= 2:
                prev, last = hist.iloc[-2], hist.iloc[-1]
                percent_change = ((last["Close"] - prev["Close"]) / prev["Close"]) * 100
                data.append({
                    "SYMBOL": ticker.replace('.NS', ''),
                    "OPEN": last["Open"],
                    "HIGH": last["High"],
                    "LOW": last["Low"],
                    "CLOSE": last["Close"],
                    "PREVCLOSE": prev["Close"],
                    "PERCENT_CHANGE": percent_change
                })
        return pd.DataFrame(data)
    except:
        return None

def process_uploaded_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if "PERCENT_CHANGE" not in df.columns and "PREVCLOSE" in df.columns and "CLOSE" in df.columns:
            df["PERCENT_CHANGE"] = ((df["CLOSE"] - df["PREVCLOSE"]) / df["PREVCLOSE"]) * 100
        return df
    except:
        return None

def show_summary_report():
    st.title("📅 Daily Summary Report (Post-Market)")
    
    df = load_nse_bhavcopy_data()
    
    if df is None:
        st.warning("⚠️ NSE Bhavcopy failed. Trying fallback (yfinance)...")
        df = load_from_yfinance()
    
    if df is None:
        st.warning("⚠️ yFinance also failed. You can upload a CSV file instead.")
        uploaded_file = st.file_uploader("📁 Upload your Bhavcopy CSV file", type=['csv'])
        if uploaded_file:
            df = process_uploaded_csv(uploaded_file)
    
    if df is None:
        st.error("❌ No valid data found.")
        return

    tab1, tab2, tab3 = st.tabs(["🔼 Top 100 Gainers", "🔽 Top 100 Losers", "📊 All Stocks"])

    with tab1:
        top_gainers = df.sort_values("PERCENT_CHANGE", ascending=False).head(100)
        st.subheader("🔼 Top 100 Gainers")
        st.dataframe(top_gainers.reset_index(drop=True), use_container_width=True)

    with tab2:
        top_losers = df.sort_values("PERCENT_CHANGE", ascending=True).head(100)
        st.subheader("🔽 Top 100 Losers")
        st.dataframe(top_losers.reset_index(drop=True), use_container_width=True)

    with tab3:
        st.subheader("📊 All Stocks (Sortable/Searchable)")
        st.dataframe(df.sort_values("SYMBOL").reset_index(drop=True), use_container_width=True)
