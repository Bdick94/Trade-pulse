import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PulseTrade", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background: #0A0A0A; color: #F0F0F0; }
    .main-header { font-size: 2.4rem; font-weight: 700; background: linear-gradient(90deg, #00FF88, #00CCFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .section { background: #141414; border-radius: 20px; padding: 20px; margin: 15px 0; }
    .live-badge { background: #FF2D55; color: white; padding: 6px 18px; border-radius: 30px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">PulseTrade</h1>', unsafe_allow_html=True)
st.caption("Swipe or tap below • Real-time social trading")

# Navigation Pills
nav = st.radio("Navigate", ["Portfolio", "Discover", "Community", "Live"], horizontal=True, label_visibility="collapsed")

portfolio = ["ATAI", "CHWY", "SMR"]
watchlist = ["NVDA", "AMD", "META", "TSLA", "RKLB", "CIFR"]

@st.cache_data(ttl=60)
def get_stock(ticker):
    try:
        s = yf.Ticker(ticker)
        return s.info, s.history(period="5d")
    except:
        return {}, pd.DataFrame()

# ====================== PORTFOLIO ======================
if nav == "Portfolio":
    st.subheader("Your Holdings")
    cols = st.columns(3)
    for i, t in enumerate(portfolio):
        info, _ = get_stock(t)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        change = info.get('regularMarketChangePercent', 0)
        with cols[i % 3]:
            st.metric(t, f"${price:.2f}", f"{change:.2f}%")

# ====================== DISCOVER ======================
elif nav == "Discover":
    selected = st.multiselect("Compare", watchlist + portfolio, default=["ATAI","NVDA","SMR"])
    data = {t: get_stock(t) for t in selected}
    
    cols = st.columns(len(selected))
    for i, (t, (info, _)) in enumerate(data.items()):
        with cols[i]:
            st.metric(t, f"${info.get('currentPrice',0):.2f}", f"{info.get('regularMarketChangePercent',0):.2f}%")
    
    fig = go.Figure()
    for t, (_, hist) in data.items():
        if not hist.empty:
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=t))
    st.plotly_chart(fig, use_container_width=True)

# ====================== COMMUNITY ======================
elif nav == "Community":
    st.subheader("💬 Trending Ideas")
    st.markdown("**ATAI** • Strong buy on FDA progress • Bullish +18%")
    st.markdown("**NVDA** • AI demand exploding • Very Bullish")
    st.markdown("**SMR** • Nuclear contracts coming • Bullish")

# ====================== LIVE ======================
elif nav == "Live":
    st.subheader("📡 Live Rooms")
    st.markdown('<span class="live-badge">LIVE</span> NVDA AI Summit', unsafe_allow_html=True)
    st.video("https://www.youtube.com/embed/dQw4w9wgxcq")  # Replace later
    chat = st.text_input("Send message to live room...")
    if st.button("Send"):
        st.success("Sent to live audience!")

st.caption("Built for mobile • Pull down to refresh")
