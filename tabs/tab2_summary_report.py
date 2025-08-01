import streamlit as st
import pandas as pd
import yfinance as yf
import io

DEFAULT_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "SBIN.NS", "LT.NS", "AXISBANK.NS", "KOTAKBANK.NS", "ITC.NS",
    "BAJFINANCE.NS", "BHARTIARTL.NS", "MARUTI.NS", "WIPRO.NS", "HCLTECH.NS",
    "ULTRACEMCO.NS", "ASIANPAINT.NS", "HINDUNILVR.NS", "POWERGRID.NS", "NTPC.NS"
]

@st.cache_data(show_spinner=False)
def fetch_data(symbols):
    df = yf.download(
        tickers=symbols,
        period="2d",
        interval="1d",
        group_by="ticker",
        threads=True,
        progress=False
    )
    
    rows = []
    for symbol in symbols:
        try:
            hist = df[symbol]
            if hist.shape[0] < 2:
                continue
            prev_close = hist['Close'].iloc[0]
            latest = hist.iloc[1]
            pct_change = ((latest['Close'] - prev_close) / prev_close) * 100
            rsi = compute_rsi(hist['Close'].values)
            sma20 = hist['Close'].rolling(20).mean().iloc[-1]
            rows.append({
                "Symbol": symbol,
                "Close": latest['Close'],
                "% Change": round(pct_change, 2),
                "Volume": latest['Volume'],
                "RSI": round(rsi, 2) if rsi else None,
                "SMA 20": round(sma20, 2) if pd.notna(sma20) else None
            })
        except Exception:
            continue
    df_final = pd.DataFrame(rows)
    return df_final

def compute_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    delta = pd.Series(prices).diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean().iloc[-1]
    avg_loss = loss.rolling(window=period).mean().iloc[-1]
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

@st.cache_data
def convert_df(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Summary")
    return output.getvalue()

def show():
    st.header("📅 Daily Summary Report")
    st.markdown("This section shows top gainers, losers, and volume leaders.")

    uploaded = st.file_uploader("Upload CSV of symbols", type=["csv"])
    if uploaded:
        uploaded_df = pd.read_csv(uploaded)
        symbols = uploaded_df.iloc[:, 0].astype(str).tolist()
    else:
        symbols = DEFAULT_SYMBOLS

    data = fetch_data(symbols)
    if data.empty:
        st.warning("No data fetched.")
        return

    st.sidebar.subheader("🔍 Filters")
    min_volume = st.sidebar.slider("Minimum Volume", 0, int(data['Volume'].max()), 0)
    rsi_range = st.sidebar.slider("RSI Range", 0, 100, (0, 100))
    sma_filter = st.sidebar.checkbox("Show only stocks above SMA 20", value=False)

    filtered = data[
        (data['Volume'] >= min_volume) &
        (data['RSI'].between(rsi_range[0], rsi_range[1]))
    ]
    if sma_filter:
        filtered = filtered[filtered['Close'] > filtered['SMA 20']]

    tab1, tab2, tab3 = st.tabs(["📈 Top Gainers", "📉 Top Losers", "🔥 Volume Leaders"])

    with tab1:
        gainers = filtered.sort_values(by="% Change", ascending=False).head(50)
        st.dataframe(gainers.reset_index(drop=True), use_container_width=True)

    with tab2:
        losers = filtered.sort_values(by="% Change", ascending=True).head(50)
        st.dataframe(losers.reset_index(drop=True), use_container_width=True)

    with tab3:
        vol_leaders = filtered.sort_values(by="Volume", ascending=False).head(50)
        st.dataframe(vol_leaders.reset_index(drop=True), use_container_width=True)

    excel = convert_df(filtered)
    st.download_button(
        "📥 Download Filtered Summary to Excel",
        data=excel,
        file_name="summary_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
