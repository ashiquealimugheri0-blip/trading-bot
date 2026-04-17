import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="Quotex AI Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    div.stButton > button { width: 100%; background-color: #1c2128; color: #adbac7; border: 1px solid #444c56; font-weight: bold; }
    div.stButton > button:hover { border-color: #00b97a; color: #00b97a; }
    </style>
    """, unsafe_allow_html=True)

# --- Telegram Setup ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnx13z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try: requests.get(url, timeout=5)
    except: pass

st.title("📊 Quotex Pro AI Dashboard")

# --- Market Selection ---
if 'symbol' not in st.session_state:
    st.session_state.symbol = "EURUSD=X"

m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
if m_col1.button("EUR/USD"): st.session_state.symbol = "EURUSD=X"
if m_col2.button("GBP/USD"): st.session_state.symbol = "GBPUSD=X"
if m_col3.button("USD/JPY"): st.session_state.symbol = "JPY=X"
if m_col4.button("USD/BDT"): st.session_state.symbol = "BDT=X"
if m_col5.button("BTC/USD"): st.session_state.symbol = "BTC-USD"

current_symbol = st.session_state.symbol
# Timeframe check: 1m aksar block hota hai, isliye 5m zyada stable hai
timeframe = st.sidebar.selectbox("Select Timeframe", ("1m", "5m", "15m"), index=0)

placeholder = st.empty()

while True:
    try:
        # Data Download (Period '1d' and Interval '1m/5m')
        data = yf.download(current_symbol, period="1d", interval=timeframe, progress=False, auto_adjust=True)
        
        if not data.empty and len(data) > 5:
            df = data.copy()
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Indicators
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_200'] = ta.ema(df['Close'], length=200)
            
            price = float(df['Close'].iloc[-1])
            rsi_val = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 50.0
            ema_val = float(df['EMA_200'].iloc[-1]) if not pd.isna(df['EMA_200'].iloc[-1]) else price

            with placeholder.container():
                st.write(f"### Live Chart: {current_symbol} ({timeframe})")
                
                # Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Live Price", f"{price:.5f}")
                c2.metric("RSI (14)", f"{rsi_val:.2f}")
                c3.metric("EMA 200", f"{ema_val:.5f}")

                # Candle Chart Fix
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    increasing_line_color='#00e676', 
                    decreasing_line_color='#ff1744'
                )])
                
                fig.update_layout(
                    template="plotly_dark",
                    xaxis_rangeslider_visible=False,
                    height=500,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Signal Section
                signal, bg = "SCANNING MARKET...", "#1c2128"
                if price > ema_val and rsi_val < 30:
                    signal, bg = "🟢 STRONG UP (CALL)", "#00e676"
                    send_telegram_msg(f"🚀 CALL SIGNAL: {current_symbol} @ {price}")
                elif price < ema_val and rsi_val > 70:
                    signal, bg = "🔴 STRONG DOWN (PUT)", "#ff1744"
                    send_telegram_msg(f"📉 PUT SIGNAL: {current_symbol} @ {price}")

                st.markdown(f"<div style='text-align: center; background-color: {bg}; color: white; padding: 20px; border-radius: 10px; font-size: 24px; font-weight: bold;'>{signal}</div>", unsafe_allow_html=True)
                st.info(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")

        else:
            st.warning(f"Waiting for market data for {current_symbol}... Try changing timeframe.")

    except Exception as e:
        st.error(f"Error: {e}. Retrying in 10s...")
        time.sleep(10)
        continue

    time.sleep(15) # Refresh every 15 seconds
    st.rerun()
