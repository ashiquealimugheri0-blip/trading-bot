import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Quotex AI Signals", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    [data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- Settings ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnx13z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url, timeout=5)
    except:
        pass

st.title("📊 Quotex Pro AI Dashboard")
symbol = st.sidebar.text_input("Asset Symbol", "EURUSD=X")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=0)

placeholder = st.empty()

# Main Loop
while True:
    with placeholder.container():
        try:
            # Data Fetching
            df = yf.download(symbol, period="1d", interval=timeframe, progress=False)
            
            if not df.empty and len(df) > 10:
                # Indicators
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_200'] = ta.ema(df['Close'], length=200)
                
                # Get latest values
                price = float(df['Close'].iloc[-1])
                rsi_val = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 0
                ema_val = float(df['EMA_200'].iloc[-1]) if not pd.isna(df['EMA_200'].iloc[-1]) else 0

                # Metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Live Price", f"{price:.5f}")
                c2.metric("RSI (14)", f"{rsi_val:.2f}")
                c3.metric("EMA 200", f"{ema_val:.5f}")

                # Candlestick Chart
                fig = go.Figure(data=[go.Candlestick(x=df.index,
                                open=df['Open'], high=df['High'],
                                low=df['Low'], close=df['Close'],
                                increasing_line_color='#00b97a', 
                                decreasing_line_color='#ff3b3b')])
                fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)

                # Signal Logic
                signal = "WAITING"
                bg = "#161b22"
                
                if ema_val > 0:
                    if price > ema_val and rsi_val < 35:
                        signal = "🟢 UP (CALL)"
                        bg = "#00b97a"
                        send_telegram_msg(f"🚀 UP: {symbol} @ {price}")
                    elif price < ema_val and rsi_val > 65:
                        signal = "🔴 DOWN (PUT)"
                        bg = "#ff3b3b"
                        send_telegram_msg(f"📉 DOWN: {symbol} @ {price}")

                st.markdown(f"<div style='text-align: center; background-color: {bg}; padding: 20px; border-radius: 10px; font-size: 24px;'>{signal}</div>", unsafe_allow_html=True)
            else:
                st.info("Market data load ho raha hai...")
                
        except Exception as e:
            st.error(f"Error: {e}")

    # Time wait aur refresh
    time.sleep(30)
    st.rerun()
