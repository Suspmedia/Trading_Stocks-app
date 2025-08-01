import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import io

@st.cache_data(ttl=3600)
def get_nifty500_list():
    return [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 'HINDUNILVR.NS', 'SBIN.NS',
        'AXISBANK.NS', 'BAJFINANCE.NS', 'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'ASIANPAINT.NS',
        'SUNPHARMA.NS', 'MARUTI.NS', 'NTPC.NS', 'ULTRACEMCO.NS', 'TITAN.NS', 'HCLTECH.NS',
        'TECHM.NS', 'POWERGRID.NS', 'ONGC.NS', 'TATASTEEL.NS', 'JSWSTEEL.NS', 'WIPRO.NS',
        'COALINDIA.NS', 'NESTLEIND.NS', 'HDFCLIFE.NS', 'BPCL.NS', 'ADANIENT.NS', 'EICHERMOT.NS',
        'DRREDDY.NS', 'DIVISLAB.NS', 'CIPLA.NS', 'BHARTIARTL.NS', 'GRASIM.NS', 'BRITANNIA.NS',
        'BAJAJ-AUTO.NS', 'HINDALCO.NS', 'UPL.NS', 'SHREECEM.NS', 'TATACONSUM.NS', 'M&M.NS'
    ]

@st.cache_data(ttl=3600)
def fetch_data(symbols, period="1d", interval="1d"):
    df_list = []
    for symbol in symbols:
        try:
            data = yf.download(symbol, period=period, interval=interval, progress=False)
            if not data.empty:
                latest = data.iloc[-1]
                prev_close = data.iloc[-2]["Close"] if len(data) > 1 else latest["Open"]
                pct_change = ((latest["Close"] - prev_close) / prev_close) * 100 if prev_close else 0
                df_list.append({
                    "Symbol": symbol,
                    "Open": latest["Open"],
                    "High": latest["High"],
                    "Low": latest["Low"],
                    "Close": latest["Close"],
                    "Volume": latest["Volume"],
                    "% Change": round(pct_change, 2)
                })
        except Exception:
            continue
    df = pd.DataFrame(df_list)
    df = df.dropna(subset=["% Change", "Close", "Volume"])  # Clean rows with missing values
    df = df[pd.to_numeric(df["% Change"], errors="coerce").notnull()]  # Keep numeric only
    return df

def show():
    st.header("📅 Daily Summary Report")

    mode = st.radio("Data Source", ["Preloaded NIFTY 500", "Upload Full NSE List (CSV)"])

    if mode == "Upload Full NSE List (CSV)":
        uploaded_file = st.file_uploader("Upload NSE CSV (with Symbol column)", type=["csv"])
        if uploaded_file:
            df_csv = pd.read_csv(uploaded_file)
            if 'Symbol' in df_csv.columns:
                symbols = [s.strip().upper() for s in df_csv['Symbol'].tolist()]
                symbols = [s if s.endswith('.NS') else s + ".NS" for s in symbols]
            else:
                st.error("Uploaded CSV must have a 'Symbol' column.")
                return
        else:
            st.warning("Please upload a CSV file to proceed.")
            return
    else:
        symbols = get_nifty500_list()

    with st.spinner("Fetching stock data..."):
        data = fetch_data(symbols)

    if data.empty:
        st.error("No stock data fetched. Please check your symbols or try again.")
        return

    try:
        gainers = data.sort_values(by="% Change", ascending=False).head(50).reset_index(drop=True)
        losers = data.sort_values(by="% Change", ascending=True).head(50).reset_index(drop=True)
        volume_leaders = data.sort_values(by="Volume", ascending=False).head(50).reset_index(drop=True)
        overbought = data[data["% Change"] > 5].sort_values(by="% Change", ascending=False)
        oversold = data[data["% Change"] < -5].sort_values(by="% Change")
    except Exception as e:
        st.error(f"Error in processing data: {e}")
        return

    st.markdown("### 📊 Top 50 Gainers & Losers")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Gainers", "📉 Losers", "🔊 Volume", "📈 Overbought", "📉 Oversold"])

    with tab1:
        st.dataframe(gainers, use_container_width=True)

    with tab2:
        st.dataframe(losers, use_container_width=True)

    with tab3:
        st.dataframe(volume_leaders, use_container_width=True)

    with tab4:
        st.dataframe(overbought, use_container_width=True)

    with tab5:
        st.dataframe(oversold, use_container_width=True)

    # Export
    st.markdown("### 📁 Download Summary")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        gainers.to_excel(writer, index=False, sheet_name='Top Gainers')
        losers.to_excel(writer, index=False, sheet_name='Top Losers')
        volume_leaders.to_excel(writer, index=False, sheet_name='Top Volume')
        overbought.to_excel(writer, index=False, sheet_name='Overbought')
        oversold.to_excel(writer, index=False, sheet_name='Oversold')
        writer.close()
    st.download_button("📥 Download Excel Report", data=buffer.getvalue(), file_name="daily_summary_report.xlsx", mime="application/vnd.ms-excel")
