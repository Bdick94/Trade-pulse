import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PulseTrade", layout="wide", initial_sidebar_state="collapsed")

# Premium CSS
st.markdown("""
<style>
    .stApp { background: #0A0A0A; color: #F0F0F0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .main-header { font-size: 2.2rem; font-weight: 700; background: linear-gradient(90deg, #00FF88, #00CCFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .card { background: #141414; border-radius: 16px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); margin-bottom: 20px; }
    .live-badge { background: #FF2D55; color: white; padding: 6px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 600; }
    .metric-value { font-size: 1.8rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">PulseTrade</h1>', unsafe_allow_html=True)
st.caption("Social Trading • Intelligence • Community")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Portfolio", "🔍 Discover", "💬 Community", "📡 Live"])

portfolio = ["ATAI", "CHWY", "SMR"]
watchlist = ["NVDA", "AMD", "META", "TSLA", "RKLB", "CIFR", "IREN"]

@st.cache_data(ttl=60)
def get_stock(ticker):
    try:
        s = yf.Ticker(ticker)
        return s.info, s.history(period="5d")
    except:
        return {}, pd.DataFrame()

# ====================== PORTFOLIO TAB ======================
with tab1:
    st.markdown('<div class="card"><h3>Your Holdings</h3></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, t in enumerate(portfolio):
        info, _ = get_stock(t)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        change = info.get('regularMarketChangePercent', 0)
        with cols[i]:
            delta_color = "normal" if change >= 0 else "inverse"
            st.metric(label=t, value=f"${price:.2f}", delta=f"{change:.2f}%", delta_color=delta_color)

# ====================== DISCOVER TAB ======================
with tab2:
    selected = st.multiselect("Compare Stocks", watchlist + portfolio, default=["ATAI", "NVDA", "SMR"])
    data = {t: get_stock(t) for t in selected}
    
    mcols = st.columns(len(selected))
    for i, (t, (info, _)) in enumerate(data.items()):
        with mcols[i]:
            st.metric(t, f"${info.get('currentPrice',0):.2f}", f"{info.get('regularMarketChangePercent',0):.2f}%")
    
    fig = go.Figure()
    for t, (_, hist) in data.items():
        if not hist.empty:
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=t, mode='lines+markers'))
    fig.update_layout(height=450, template="plotly_dark", margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ====================== COMMUNITY TAB ======================
with tab3:
    st.subheader("💬 Trending Ideas")
    ideas = [
        ("ATAI", "Strong buy on FDA progress", "Bullish", "+18%"),
        ("NVDA", "AI demand still exploding", "Very Bullish", "+2.4%"),
        ("SMR", "Nuclear contracts incoming", "Bullish", "-1.8%")
    ]
    for stock, idea, sentiment, perf in ideas:
        st.markdown(f"""
        <div class="card">
            <strong>{stock}</strong> • {sentiment}<br>
            {idea} <span style="color:#00FF88">{perf}</span>
        </div>
        """, unsafe_allow_html=True)

# ====================== LIVE TAB ======================
with tab4:
    st.subheader("📡 Live Rooms")
    st.markdown('<span class="live-badge">LIVE NOW</span> **NVDA AI &amp; Chips Discussion**', unsafe_allow_html=True)
    
    st.video("https://www.youtube.com/embed/dQw4w9wgxcq")  # ← Replace with real stream later
    
    st.text_input("💬 Say something in the live room...", placeholder="This nuclear thesis is wild...")
    if st.button("Send to Live"):
        st.success("Message sent to live audience!")

st.sidebar.success("Premium Experience • v0.3")
st.caption("Made for you • Refresh for live data")
