import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

@st.cache_data(show_spinner=False)
def get_nifty500_symbols():
    return pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty500list.csv")["Symbol"].apply(lambda x: x + ".NS").tolist()

@st.cache_data(show_spinner=True)
def fetch_data(symbols):
    tickers = yf.Tickers(" ".join(symbols))
    data = []
    for symbol in symbols:
        try:
            ticker = tickers.tickers[symbol]
            hist = ticker.history(period="2d", interval="1d")
            if len(hist) < 2:
                continue
            prev_close = hist['Close'].iloc[0]
            latest = hist.iloc[-1]
            pct_change = ((latest['Close'] - prev_close) / prev_close) * 100
            info = ticker.info
            pe = info.get("trailingPE", None)
            hist_month = ticker.history(period="1mo")
            sma20 = hist_month['Close'].rolling(20).mean().iloc[-1] if len(hist_month) >= 20 else None
            delta = hist_month['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(14).mean().iloc[-1]
            avg_loss = loss.rolling(14).mean().iloc[-1]
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))

            data.append({
                "Symbol": symbol.replace(".NS", ""),
                "Close": latest['Close'],
                "% Change": pct_change,
                "Volume": latest['Volume'],
                "P/E Ratio": pe,
                "SMA 20": sma20,
                "RSI": rsi
            })
        except Exception:
            continue
    return pd.DataFrame(data)

def show():
    st.header("📅 Daily Summary Report")

    st.markdown("### 🔍 Choose Data Source")
    use_custom = st.checkbox("Upload your own stock list (CSV)", value=False)

    if use_custom:
        uploaded = st.file_uploader("Upload CSV with column 'Symbol'", type=["csv"])
        if uploaded:
            user_df = pd.read_csv(uploaded)
            symbols = user_df['Symbol'].dropna().tolist()
            symbols = [s if s.endswith(".NS") else s + ".NS" for s in symbols]
        else:
            st.warning("Please upload a valid CSV file.")
            return
    else:
        symbols = get_nifty500_symbols()

    st.markdown("### 📥 Fetching Data...")
    data = fetch_data(symbols)
    if data.empty:
        st.error("❌ No data fetched.")
        return

    st.markdown("### 📊 Summary Filters")

    # Add filters
    min_rsi, max_rsi = st.slider("RSI Range", 0, 100, (30, 70))
    min_pe, max_pe = st.slider("P/E Ratio Range", 0.0, 100.0, (0.0, 60.0))

    filtered = data[
        (data["RSI"].between(min_rsi, max_rsi)) &
        (data["P/E Ratio"].between(min_pe, max_pe, inclusive="both"))
    ]

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Gainers", "📉 Losers", "🔥 Volume Leaders", "📘 Fundamentals"])

    with tab1:
        st.subheader("Top 50 Gainers")
        gainers = filtered.sort_values(by="% Change", ascending=False).head(50).reset_index(drop=True)
        st.dataframe(gainers)
    
    with tab2:
        st.subheader("Top 50 Losers")
        losers = filtered.sort_values(by="% Change", ascending=True).head(50).reset_index(drop=True)
        st.dataframe(losers)

    with tab3:
        st.subheader("Top 50 Volume Leaders")
        volume = filtered.sort_values(by="Volume", ascending=False).head(50).reset_index(drop=True)
        st.dataframe(volume)

    with tab4:
        st.subheader("Fundamental Overview (P/E, RSI, SMA)")
        st.dataframe(filtered.sort_values(by="P/E Ratio", na_position="last").reset_index(drop=True))

    # Excel Export
    st.markdown("### 📤 Export Summary to Excel")
    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    excel = convert_df(filtered)
    st.download_button("📥 Download Excel", data=excel, file_name="summary_report.xlsx")

