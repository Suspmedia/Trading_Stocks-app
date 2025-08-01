import streamlit as st

# Load tab modules from the 'tabs' folder
from tabs.tab2_summary_report import show_summary_report
# You can add other tabs similarly when ready

# --- App Title ---
st.set_page_config(page_title="📈 Indian Stock Market Analyzer", layout="wide")
st.title("📊 Indian Stock Market Analyzer")
st.markdown("""
Welcome to the all-in-one Indian Stock Market data analysis app!
""")

# --- Tab Selection ---
tabs = [
    "📈 Tab 1 - Stock Market Charts (Coming Soon)",
    "📅 Tab 2 - Daily Summary Report",
    "🔍 Tab 3 - Stock History & Forecast (Coming Soon)",
    "📊 Tab 4 - Options Analysis (Coming Soon)",
    "📡 Tab 5 - Signal Generator (Coming Soon)",
    "🌐 Tab 6 - Global Exchanges (Coming Soon)",
    "📊 Tab 7 - Advanced Indicators (Coming Soon)"
]

selected_tab = st.sidebar.radio("📁 Select Analysis Tab", tabs)

# --- Route to Tab Logic ---
if selected_tab == tabs[1]:  # Tab 2
    show_summary_report()
else:
    st.info("🛠️ This tab is under development. Please check back soon.")
