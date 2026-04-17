import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Quotex AI Pro", layout="wide")

# Custom CSS for Professional Buttons
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    div.stButton > button {
        width: 100%;
        background-color: #1c2128;
        color: #adbac7;
        border: 1px solid #444c56;
        border-radius: 4px;
        padding: 10px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        border-color: #00b97a;
        color: #00b97a;
        background-color: #22272e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Settings ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnx13z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try: requests.get(url, timeout=5)
    except: pass

st.title("📊 Quotex Pro AI Dashboard")

# --- Market Selection Buttons ---
st.write("### 💱 Select Trading Pair")
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)

if 'symbol' not in st.session_state:
    st.session_state.symbol = "EURUSD=X"

# Buttons with Pairs
if m_col1.button("EUR/USD"): st.session_state.symbol = "EURUSD=X"
if m_col2.button("GBP/USD"): st.session_state.symbol = "GBPUSD=X"
if m_col3.button("USD/JPY"): st.session_state.symbol = "JPY=X"
if m_col4.button("USD/BDT"): st.session_state.symbol = "BDT=X"
if m_col5.button("BTC/USD"): st.session_state.symbol = "BTC-USD"

current_symbol = st.session_state.symbol
st.sidebar.markdown(f"## Active: **{current_symbol}**")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=0)

dashboard = st.empty()

while True:
    try:
        # Download Data
        data = yf.download(current_symbol, period="1d", interval=timeframe, progress=False, auto_adjust=True)
        
        if not data.empty and len(data) > 20:
            df = data.copy()
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Indicators
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_200'] = ta.ema(df['Close'], length=200)
            
            price = float(df['Close'].iloc[-1])
            rsi_val = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 50.0
            ema_val = float(df['EMA_200'].iloc[-1]) if not pd.isna(df['EMA_200'].iloc[-1]) else price

            with dashboard.container():
                # Display Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Live Price", f"{price:.5f}")
                c2.metric("RSI (14)", f"{rsi_val:.2f}")
                c3.metric("EMA 200", f"{ema_val:.5f}")

                # Chart
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index, open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'],
                    increasing_line_color='#00b97a', decreasing_line_color='#ff3b3b'
                )])
                fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True)

                # Signal Logic
                signal = "SCANNING..."
                bg = "#1c2128"
                if price > ema_val and rsi_val < 35:
                    signal = "🟢 CALL (UP)"
                    bg = "#00b97a"
                    send_telegram_msg(f"🚀 CALL: {current_symbol} @ {price}")
                elif price < ema_val and rsi_val > 65:
                    signal = "🔴 PUT (DOWN)"
                    bg = "#ff3b3b"
                    send_telegram_msg(f"📉 PUT: {current_symbol} @ {price}")

                st.markdown(f"<div style='text-align: center; background-color: {bg}; padding: 25px; border-radius: 8px; font-size: 28px; font-weight: bold;'>{signal}</div>", unsafe_allow_html=True)
        
        else:
            st.info("🔄 Connecting to market... Please wait.")

    except Exception as e:
        st.error(f"Connection Pause... Retrying in 60s")
        time.sleep(60)
        continue

    time.sleep(60)
    st.rerun()
