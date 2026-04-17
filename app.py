import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- Page Config (Quotex Style Dark Theme) ---
st.set_page_config(page_title="Quotex AI Signals", layout="wide")

# Custom CSS for Dark UI
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 30px; }
    .stButton>button { width: 100%; background-color: #00b97a; color: white; border-radius: 5px; }
    .css-1offfwp { background-color: #161b22 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Telegram Setup ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnx13z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try: requests.get(url)
    except: pass

# --- UI Header ---
st.title("📊 Quotex Pro AI Dashboard")
symbol = st.sidebar.text_input("Asset (e.g. EURUSD=X)", "EURUSD=X")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=0)

# Main Container
placeholder = st.empty()

while True:
    with placeholder.container():
        # Fetch Data
        df = yf.download(symbol, period="1d", interval=timeframe, progress=False)
        
        if not df.empty:
            # Technical Indicators
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_200'] = ta.ema(df['Close'], length=200)
            last_row = df.iloc[-1]
            
            price = last_row['Close']
            rsi = last_row['RSI']
            ema = last_row['EMA_200']

            # --- Quotex Style Chart ---
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                            open=df['Open'], high=df['High'],
                            low=df['Low'], close=df['Close'],
                            increasing_line_color='#00b97a', decreasing_line_color='#ff3b3b')])
            
            fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig, use_container_width=True)

            # --- Metrics & Signals ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Live Price", f"{price:.5f}")
            col2.metric("RSI (14)", f"{rsi:.2f}")
            
            # Logic for Quotex Style Signal
            signal = "WAITING"
            color = "white"
            
            if price > ema and rsi < 35:
                signal = "UP (CALL)"
                color = "#00b97a"
            elif price < ema and rsi > 65:
                signal = "DOWN (PUT)"
                color = "#ff3b3b"

            st.markdown(f"<h1 style='text-align: center; color: {color}; border: 2px solid {color}; padding: 10px;'>Signal: {signal}</h1>", unsafe_allow_html=True)

            # Send Telegram if Signal exists
            if signal != "WAITING":
                send_telegram_msg(f"🚀 QUOTEX SIGNAL: {symbol}\nAction: {signal}\nPrice: {price}")

        st.write(f"Refreshed at: {pd.Timestamp.now().strftime('%H:%M:%S')}")
        time.sleep(10)
        st.rerun()
