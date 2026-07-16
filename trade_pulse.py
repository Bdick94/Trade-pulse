import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="PulseTrade", layout="wide", initial_sidebar_state="collapsed")

# Clean iOS-friendly CSS
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .metric { background: #1E1F26; border-radius: 12px; padding: 12px; }
    .live-badge { background: #FF2D55; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 PulseTrade")
st.caption("Social Trading • Live • Yours")

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio", "🔍 Compare", "💬 Feed", "📡 Live"])

# ====================== DATA ======================
portfolio = ["ATAI", "CHWY", "SMR"]
watchlist = ["CHWY", "CIFR", "IREN", "SMR", "RKLB", "NVDA", "AMD", "META"]

@st.cache_data(ttl=60)
def get_stock(ticker):
    try:
        s = yf.Ticker(ticker)
        return s.info, s.history(period="5d")
    except:
        return {}, pd.DataFrame()

# ====================== TAB 1: PORTFOLIO ======================
with tab1:
    st.subheader("Your Portfolio")
    cols = st.columns(3)
    for i, t in enumerate(portfolio):
        info, _ = get_stock(t)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        change = info.get('regularMarketChangePercent', 0)
        with cols[i % 3]:
            st.metric(t, f"${price:.2f}", f"{change:.2f}%")

# ====================== TAB 2: COMPARE ======================
with tab2:
    selected = st.multiselect("Select stocks", watchlist + portfolio, default=portfolio)
    data = {t: get_stock(t) for t in selected}
    
    # Metrics
    mcols = st.columns(len(selected))
    for i, (t, (info, _)) in enumerate(data.items()):
        with mcols[i]:
            st.metric(t, f"${info.get('currentPrice', 0):.2f}", 
                     f"{info.get('regularMarketChangePercent', 0):.2f}%")
    
    # Chart
    fig = go.Figure()
    for t, (_, hist) in data.items():
        if not hist.empty:
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=t))
    st.plotly_chart(fig, use_container_width=True)

# ====================== TAB 3: FEED ======================
with tab3:
    st.subheader("💬 Community Feed")
    for stock in ["ATAI", "NVDA", "SMR"]:
        st.markdown(f"**{stock}**")
        st.caption("Bullish on nuclear catalysts • +12% today")
        if st.button("💬 Add comment", key=stock):
            st.success("Posted! (demo)")
        st.divider()

# ====================== TAB 4: LIVE ======================
with tab4:
    st.subheader("📡 Live Streams")
    st.markdown('<span class="live-badge">LIVE</span> **NVDA AI Summit**', unsafe_allow_html=True)
    
    # YouTube/Twitch embed example
    st.video("https://www.youtube.com/embed/dQw4w9wgxcq")  # Replace with real stream URL later
    
    st.subheader("Live Chat")
    chat = st.text_input("Send message to live room...")
    if st.button("Send"):
        st.info("Message sent to live room (demo)")
    
    st.caption("More live rooms: ATAI Psychedelics • SMR Nuclear • TSLA Robotaxi")

st.sidebar.success("PulseTrade v0.2 • Livestreaming enabled")
st.caption("Refresh for latest prices • Built for mobile")
