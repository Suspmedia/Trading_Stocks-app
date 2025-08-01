import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import io

NIFTY100 = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'LT.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'BAJFINANCE.NS',
    'HCLTECH.NS', 'WIPRO.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS', 'DMART.NS', 'NESTLEIND.NS',
    'SUNPHARMA.NS', 'MARUTI.NS', 'ULTRACEMCO.NS', 'TITAN.NS', 'TECHM.NS', 'NTPC.NS',
    'ADANIENT.NS', 'ADANIGREEN.NS', 'ADANIPORTS.NS', 'BAJAJFINSV.NS', 'CIPLA.NS',
    'DIVISLAB.NS', 'GRASIM.NS', 'JSWSTEEL.NS', 'POWERGRID.NS', 'ONGC.NS', 'COALINDIA.NS',
    'BPCL.NS', 'HINDALCO.NS', 'IOC.NS', 'INDUSINDBK.NS', 'HDFCLIFE.NS', 'ICICIPRULI.NS',
    'SBILIFE.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS', 'BAJAJ-AUTO.NS', 'TATAMOTORS.NS',
    'TATASTEEL.NS', 'BRITANNIA.NS', 'SHREECEM.NS', 'ZOMATO.NS'
]

@st.cache_data(show_spinner="Fetching NIFTY 100 data...")
def fetch_data(symbols):
    data = yf.download(symbols, period="2d", interval="1d", group_by='ticker', progress=False)
    rows = []

    for symbol in symbols:
        try:
            df = data[symbol]
            close = df['Close'].iloc[-1]
            prev_close = df['Close'].iloc[-2]
            volume = df['Volume'].iloc[-1]
            pct_change = ((close - prev_close) / prev_close) * 100
            rsi = compute_rsi(df['Close'])
            rows.append({
                'Symbol': symbol.replace('.NS', ''),
                'Close': round(close, 2),
                'Volume': int(volume),
                '% Change': round(pct_change, 2),
                'RSI': round(rsi, 2)
            })
        except:
            continue

    return pd.DataFrame(rows)

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.isna().all() else None

@st.cache_data
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Summary')
    return output.getvalue()

def show():
    st.subheader("📅 Daily Summary Report (NIFTY 100 Only)")

    data = fetch_data(NIFTY100)

    if data.empty:
        st.warning("No data available.")
        return

    tabs = st.tabs(["🏆 Gainers", "📉 Losers", "📊 Volume Leaders", "📈 RSI", "📁 Export"])

    with tabs[0]:
        gainers = data.sort_values(by="% Change", ascending=False).head(50)
        st.dataframe(gainers, use_container_width=True)

    with tabs[1]:
        losers = data.sort_values(by="% Change", ascending=True).head(50)
        st.dataframe(losers, use_container_width=True)

    with tabs[2]:
        volume_leaders = data.sort_values(by="Volume", ascending=False).head(50)
        st.dataframe(volume_leaders, use_container_width=True)

    with tabs[3]:
        rsi_sorted = data.dropna().sort_values(by="RSI")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔻 Oversold (RSI < 30)")
            st.dataframe(rsi_sorted[rsi_sorted["RSI"] < 30], use_container_width=True)
        with col2:
            st.markdown("### 🔺 Overbought (RSI > 70)")
            st.dataframe(rsi_sorted[rsi_sorted["RSI"] > 70], use_container_width=True)

    with tabs[4]:
        excel_data = convert_df_to_excel(data)
        st.download_button(
            label="📥 Download Summary as Excel",
            data=excel_data,
            file_name="nifty100_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
