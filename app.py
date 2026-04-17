import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- Page Config (Quotex Dark UI) ---
st.set_page_config(page_title="Quotex AI Signals", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    [data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 25px; }
    .stHeader { color: #00b97a; }
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
symbol = st.sidebar.text_input("Asset Symbol", "EURUSD=X")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=0)

placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Fetch Data (Slowed down to 30s to avoid Rate Limit)
            df = yf.download(symbol, period="1d", interval=timeframe, progress=False)
            
            if not df.empty and len(df) > 10:
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['EMA_200'] = ta.ema(df['Close'], length=200)
                
                last_row = df.iloc[-1]
                price = last_row['Close']
                rsi = last_row['RSI']
                ema = last_row['EMA_200']

                # --- Metrics ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Live Price", f"{price:.5f}")
                c2.metric("RSI (14)", f"{rsi:.2f}" if not pd.isna(rsi) else "N/A")
                c3.metric("EMA 200", f"{ema:.5f}" if not pd.isna(ema) else "N/A")

                # --- Quotex Candlestick Chart ---
                fig = go.Figure(data=[go.Candlestick(x=df.index,
                                open=df['Open'], high=df['High'],
                                low=df['Low'], close=df['Close'],
                                increasing_line_color='#00b97a', 
                                decreasing_line_color='#ff3b3b')])
                fig.update_layout(template="plotly_dark", height=450, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)

                # --- Signal Logic ---
                signal = "WAITING FOR OPPORTUNITY"
                bg_color = "#161b22"
                
                if ema and rsi:
                    if price > ema and rsi < 35:
                        signal = "🟢 UP (CALL) SIGNAL"
                        bg_color = "#00b97a"
                        send_telegram_msg(f"🚀 QUOTEX UP: {symbol} at {price}")
                    elif price < ema and rsi > 65:
                        signal = "🔴 DOWN (PUT) SIGNAL"
                        bg_color = "#ff3b3b"
                        send_telegram_msg(f"📉 QUOTEX DOWN: {symbol} at {price}")

                st.markdown(f"<div style='text-align: center; background-color: {bg_color}; padding: 20px; border-radius: 10px; font-size: 24px; font-weight: bold;'>{signal}</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ Market data load nahi ho raha. Shayad market band hai ya symbol galat hai.")
                
        except Exception as e:
            st.error(f"Error: {e}")

        st.info(f"Auto-refreshing in 30 seconds... (Last check: {pd.Timestamp.now().strftime('%H:%M:%S')})")
        time.sleep(30) # Rate limit se bachne ke liye 30 seconds wait
        st.rerun()
