import streamlit as st

# Load each tab's logic
try:
    from tab2_summary_report import show_summary_report
except ModuleNotFoundError:
    def show_summary_report():
        st.error("❌ Tab 2 module (tab2_summary_report.py) not found.")

# Page Configuration
st.set_page_config(
    page_title="📊 Indian Stock Market Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📊 Indian Stock Market Analyzer")
st.markdown("Welcome to the all-in-one Indian Stock Market data analysis app!")

# Sidebar Navigation
tabs = {
    "📈 Tab 1 - Stock Market Charts": "stock_charts",
    "📅 Tab 2 - Daily Summary Report": "summary_report",
    "🔍 Tab 3 - Stock History & Forecast": "stock_forecast",
    "📊 Tab 4 - Options Analysis": "options_analysis",
    "📡 Tab 5 - Signal Generator": "signal_generator",
    "🌐 Tab 6 - Global Exchanges": "global_exchanges",
    "📊 Tab 7 - Advanced Indicators": "advanced_indicators"
}

selected_tab = st.sidebar.radio("📁 Select Analysis Tab", list(tabs.keys()))

# Main Logic
if tabs[selected_tab] == "summary_report":
    show_summary_report()

elif tabs[selected_tab] == "stock_charts":
    st.subheader("📈 Stock Market Charts (Coming Soon)")
    st.info("This tab will display live and historical charts of Indian stocks.")

elif tabs[selected_tab] == "stock_forecast":
    st.subheader("🔍 Stock Forecast & History (Coming Soon)")
    st.info("This tab will allow you to analyze past performance and predict future stock prices.")

elif tabs[selected_tab] == "options_analysis":
    st.subheader("📊 Options Chain & OI Analysis (Coming Soon)")
    st.info("This will include OI, option chain, heatmap, Greeks, and strike-level forecast.")

elif tabs[selected_tab] == "signal_generator":
    st.subheader("📡 Trading Signal Generator (Coming Soon)")
    st.info("This will generate buy/sell signals for NIFTY, BANKNIFTY, SENSEX, and stocks.")

elif tabs[selected_tab] == "global_exchanges":
    st.subheader("🌐 Global Stock Exchanges Overview (Coming Soon)")
    st.info("This tab will include summaries and indices from major global exchanges.")

elif tabs[selected_tab] == "advanced_indicators":
    st.subheader("📊 Max Pain, PCR, VIX & More (Coming Soon)")
    st.info("Advanced options metrics and volatility indicators will be analyzed here.")

else:
    st.warning("⚠️ Invalid tab selected.")
