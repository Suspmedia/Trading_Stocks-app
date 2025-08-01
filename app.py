import streamlit as st

# Page Config
st.set_page_config(
    page_title="📊 Indian Stock Market Analyzer",
    layout="wide"
)

# Import tab modules
from tabs import (
    tab1_india_stocks,
    tab2_summary_report,
    tab3_historical_forecast,
    tab4_option_analysis,
    tab5_signal_generation,
    tab6_global_markets,
    tab7_advanced_metrics,
)

# Define tabs dictionary
tabs = {
    "🏠 Home": None,
    "📈 Indian Stocks": tab1_india_stocks,
    "📅 Daily Summary Report": tab2_summary_report,
    "🔍 Stock Forecast & History": tab3_historical_forecast,
    "🧮 Option Analyzer": tab4_option_analysis,
    "🚦 Signal Generator": tab5_signal_generation,
    "🌐 Global Market Report": tab6_global_markets,
    "⚙️ Advanced Indicators": tab7_advanced_metrics,
}

# Sidebar
st.sidebar.title("📊 Stock Market Analyzer")
selected_tab = st.sidebar.radio("Go to", list(tabs.keys()))

# Home Page
if selected_tab == "🏠 Home":
    st.title("📊 Indian Stock Market Analyzer")
    st.markdown("""
    Welcome to the **Indian Stock Market Analyzer** app!

    This app helps you explore and analyze Indian stock market data, with tools for:

    - 📈 **Stock Charts & Indicators** – OHLC, Volume, SMA, RSI  
    - 📅 **Daily Summary Report** – Top gainers/losers, RSI, volume spikes  
    - 🔍 **Forecasts & Historical Data** – Visualize price trends and predictions  
    - 🧮 **Option Chain Analyzer** – Analyze OI, premiums, support/resistance  
    - 🚦 **Signal Generator** – Strategy-based trade signals (e.g., Safe, Reversal, Breakout)  
    - 🌐 **Global Market Report** – International indices and market sentiment  
    - ⚙️ **Advanced Metrics** – Technical filters, PE ratios, fundamentals  

    ---
    """)
    st.subheader("Disclaimer ⚠️")
    st.markdown("""
    - This app is intended for **informational and educational purposes only**.  
    - It does **not provide investment advice or trading recommendations**.  
    - Market data may be delayed or inaccurate.  
    - Always consult with a certified financial advisor before making investment decisions.  
    """)

    st.info("👉 Use the sidebar to navigate through different analysis tools.")
else:
    try:
        tabs[selected_tab].show()
    except AttributeError:
        st.error("⚠️ This tab is not implemented yet. Please ensure it defines a `show()` function.")
