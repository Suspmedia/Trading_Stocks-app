import streamlit as st
from tabs import (
    tab1_india_stocks, tab2_summary_report, tab3_stock_forecast,
    tab4_option_analysis, tab5_signal_generation, tab6_global_markets,
    tab7_advanced_metrics
)

st.set_page_config(page_title="Stock & Option Analytics App", layout="wide")

tab = st.sidebar.selectbox("Select a Tab", [
    "📊 Indian Stock Charts",
    "📅 Daily Summary",
    "🔍 Stock Forecast",
    "📈 Option Trading Analysis",
    "🚨 Option Signals",
    "🌐 Global Market Report",
    "🧠 Advanced Metrics"
])

if tab == "📊 Indian Stock Charts":
    tab1_india_stocks.run()
elif tab == "📅 Daily Summary":
    tab2_summary_report.run()
elif tab == "🔍 Stock Forecast":
    tab3_stock_forecast.run()
elif tab == "📈 Option Trading Analysis":
    tab4_option_analysis.run()
elif tab == "🚨 Option Signals":
    tab5_signal_generation.run()
elif tab == "🌐 Global Market Report":
    tab6_global_markets.run()
elif tab == "🧠 Advanced Metrics":
    tab7_advanced_metrics.run()