import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="PulseTrade", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0A0A0A; color: #F0F0F0; }
    .main-header { font-size: 2.5rem; font-weight: 700; background: linear-gradient(90deg, #00FF88, #00CCFF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .matrix-card { background: #141414; border-radius: 16px; padding: 20px; margin: 12px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">PulseTrade Matrix</h1>', unsafe_allow_html=True)
st.caption("Squawka-style Stock Comparison")

# Your stocks
stocks = st.multiselect("Select stocks to compare (Squawka style)", 
                       ["ATAI", "CHWY", "SMR", "NVDA", "AMD", "META", "TSLA", "RKLB"], 
                       default=["ATAI", "NVDA", "SMR"])

@st.cache_data(ttl=60)
def get_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "Price": info.get('currentPrice') or info.get('regularMarketPrice', 0),
            "Change%": round(info.get('regularMarketChangePercent', 0), 2),
            "Volume": info.get('volume', 0),
            "Market Cap": round(info.get('marketCap', 0)/1e9, 1),
            "Beta": info.get('beta', 1.0),
            "PE": info.get('trailingPE', 0),
            "Momentum": round(info.get('regularMarketChangePercent', 0) * 1.5, 1)  # Fake momentum score
        }
    except:
        return {"Price": 0, "Change%": 0, "Volume": 0, "Market Cap": 0, "Beta": 1, "PE": 0, "Momentum": 0}

data = {t: get_info(t) for t in stocks}

# ====================== MATRIX TABLE ======================
st.subheader("📊 Comparison Matrix")
df = pd.DataFrame(data).T
st.dataframe(df.style.background_gradient(cmap='RdYlGn', subset=['Change%', "Momentum"]), 
             use_container_width=True)

# ====================== RADAR CHARTS (Squawka Style) ======================
st.subheader("⚔️ Radar Comparison")
fig = make_subplots(rows=1, cols=len(stocks), specs=[[{'type': 'polar'}] * len(stocks)])

categories = ["Change%", "Momentum", "Volume (scaled)", "Market Cap", "1/Beta (stability)"]

for i, (ticker, vals) in enumerate(data.items()):
    values = [
        vals["Change%"] + 50,           # normalize
        vals["Momentum"] + 50,
        min(vals["Volume"]/1000000, 100),
        min(vals["Market Cap"], 100),
        100 - (vals["Beta"] * 20)
    ]
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=ticker
    ), row=1, col=i+1)

fig.update_layout(height=500, showlegend=True, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.caption("Higher = Better on each axis • Built for quick decisions")
