import streamlit as st
import pandas as pd
import yfinance as yf
import datetime

@st.cache_data
def load_default_watchlist():
    return [
        'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS',
        'SBIN.NS', 'AXISBANK.NS', 'LT.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BAJFINANCE.NS',
        'ASIANPAINT.NS', 'MARUTI.NS', 'WIPRO.NS', 'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS',
        'TECHM.NS', 'POWERGRID.NS', 'NESTLEIND.NS', 'HCLTECH.NS', 'NTPC.NS', 'COALINDIA.NS',
        'GRASIM.NS', 'BPCL.NS', 'ONGC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'BHARTIARTL.NS'
    ]

@st.cache_data
def fetch_stock_data(symbols):
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=7)
    data = {}
    for symbol in symbols:
        try:
            df = yf.download(symbol, start=start, end=end)
            df['Symbol'] = symbol
            data[symbol] = df
        except:
            continue
    return data

def calculate_summary(data_dict):
    summary = []
    for symbol, df in data_dict.items():
        if len(df) < 2:
            continue
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        change_pct = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
        volume = latest['Volume']
        rsi = calculate_rsi(df['Close'])[-1]
        summary.append({
            'Symbol': symbol.replace('.NS', ''),
            'Price': round(latest['Close'], 2),
            'Change %': round(change_pct, 2),
            'Volume': volume,
            'RSI': round(rsi, 2)
        })
    df_summary = pd.DataFrame(summary)
    return df_summary

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def show()
    st.header("📅 Daily Market Summary Report")

    default_watchlist = load_default_watchlist()

    uploaded_file = st.file_uploader("📥 Upload NSE full stock list CSV (optional)", type=["csv"])
    if uploaded_file:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            symbols = df_uploaded['Symbol'].apply(lambda x: x + ".NS").tolist()
            st.success(f"Loaded {len(symbols)} stocks from uploaded file.")
        except:
            st.error("❌ Error parsing uploaded CSV. Make sure it has a 'Symbol' column.")
            return
    else:
        symbols = default_watchlist
        st.info("Using preloaded NIFTY 500 stock list (faster).")

    stock_data = fetch_stock_data(symbols)
    if not stock_data:
        st.warning("⚠️ No stock data fetched. Check internet connection or stock list.")
        return

    summary_df = calculate_summary(stock_data)

    # Multiple tabs for better categorization
    tabs = st.tabs(["🔼 Top 50 Gainers", "🔽 Top 50 Losers", "📊 Top 50 Volume", "📈 Top 50 RSI"])

    with tabs[0]:
        st.subheader("🔼 Top 50 Gainers")
        st.dataframe(summary_df.sort_values(by="Change %", ascending=False).head(50), use_container_width=True)

    with tabs[1]:
        st.subheader("🔽 Top 50 Losers")
        st.dataframe(summary_df.sort_values(by="Change %").head(50), use_container_width=True)

    with tabs[2]:
        st.subheader("📊 Top 50 by Volume")
        st.dataframe(summary_df.sort_values(by="Volume", ascending=False).head(50), use_container_width=True)

    with tabs[3]:
        st.subheader("📈 Top 50 by RSI")
        st.dataframe(summary_df.sort_values(by="RSI", ascending=False).head(50), use_container_width=True)

