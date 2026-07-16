import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from textblob import TextBlob
import time

st.set_page_config(page_title="TradePulse - Stock Comparator", layout="wide")
st.title("🚀 TradePulse: Portfolio + Watchlist Comparator")
st.markdown("**Live comparison • X Sentiment • Market News**")

# ====================== YOUR DATA ======================
portfolio = {
    'ATAI': {'shares': 315, 'avg_price': 7.0},
    'CHWY': {'shares': 25, 'avg_price': 21.0},
    'SMR': {'shares': 20, 'avg_price': 8.5},
    # Add more as needed
}

watchlists = {
    "Next Buys": ["CHWY", "CIFR", "IREN", "SMR", "RKLB"],
    "Big Tech": ["NVDA", "AMD", "META", "TSLA", "AAPL"]
}

# ====================== SIDEBAR ======================
st.sidebar.header("Controls")
tickers_input = st.sidebar.text_input("Compare Tickers (comma separated)", 
                                      "ATAI,CHWY,SMR,NVDA")
selected_tickers = [t.strip().upper() for t in tickers_input.split(",")]

compare_mode = st.sidebar.selectbox("Mode", ["Comparison Table", "Sentiment + News"])

# ====================== FETCH DATA ======================
@st.cache_data(ttl=60)
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="5d")
    return info, hist

data = {}
for ticker in selected_tickers:
    try:
        info, hist = get_stock_data(ticker)
        data[ticker] = {'info': info, 'hist': hist}
    except:
        st.warning(f"Could not load {ticker}")

# ====================== MAIN DASHBOARD ======================
if data:
    cols = st.columns(len(data))
    for i, (ticker, d) in enumerate(data.items()):
        info = d['info']
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        change = info.get('regularMarketChangePercent', 0)
        with cols[i]:
            st.metric(
                label=f"**{ticker}**",
                value=f"${price:.2f}" if price else "N/A",
                delta=f"{change:.2f}%"
            )

    # Comparison Table
    if compare_mode == "Comparison Table":
        st.subheader("📊 Comparison")
        rows = []
        for ticker, d in data.items():
            info = d['info']
            rows.append({
                'Ticker': ticker,
                'Price': info.get('currentPrice'),
                'Market Cap': f"${info.get('marketCap', 0)/1e9:.1f}B",
                'P/E': info.get('trailingPE'),
                'Beta': info.get('beta'),
                '52w High': info.get('fiftyTwoWeekHigh'),
                'Volume': info.get('volume'),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

    # Charts
    st.subheader("Price Charts (Last 5 Days)")
    fig = go.Figure()
    for ticker, d in data.items():
        hist = d['hist']
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name=ticker))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ====================== LIVE NEWS & SENTIMENT ======================
st.subheader("📰 Live Market News + X Sentiment")

news_container = st.empty()
sentiment_container = st.empty()

def fetch_news():
    # Simple Yahoo Finance news (expandable to NewsAPI)
    try:
        news = []
        for ticker in selected_tickers[:3]:
            stock = yf.Ticker(ticker)
            if hasattr(stock, 'news'):
                news.extend(stock.news[:3])
        return news
    except:
        return []

def analyze_sentiment(text):
    if not text:
        return 0
    return TextBlob(text).sentiment.polarity  # -1 to 1

# Live refresh simulation
for _ in range(5):  # Demo loop - in production use st.rerun() in a loop
    with news_container:
        st.write("**Recent News**")
        news_items = fetch_news()
        for item in news_items[:5]:
            st.caption(f"• {item.get('title', 'No title')}")

    with sentiment_container:
        st.write("**X Sentiment (Simulated)**")
        sent_cols = st.columns(len(selected_tickers))
        for i, ticker in enumerate(selected_tickers):
            # In real app: query X API here
            sample_sent = analyze_sentiment(f"Positive news on {ticker} today")
            score = sample_sent * 50 + 50  # 0-100 scale
            sent_cols[i].metric(ticker, f"{score:.0f}% Bullish")
    
    time.sleep(30)  # Refresh every 30s in real version

st.info("Prototype ready! Expand with real X API keys, NewsAPI, or Polygon.io for production.")
st.caption("Built for your portfolio style • Add more features iteratively")
