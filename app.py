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

# Sidebar Navigation
tabs = {
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

# App Header
st.title("📊 Indian Stock Market Analyzer")
st.markdown("Welcome to the all-in-one Indian Stock Market data analysis app!")

# Show selected tab
try:
    tabs[selected_tab].show()
except AttributeError:
    st.error("⚠️ This tab is not implemented yet. Please ensure it defines a `show()` function.")
