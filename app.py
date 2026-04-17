import streamlit as st
import yfinance as yf
import pandas_ta as ta
import requests
import time

# --- Setup ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnxl3z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try: requests.get(url)
    except: pass

st.title("📈 Aashique Live Signals")

symbol = st.sidebar.text_input("Symbol", "EURUSD=X")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=1)

placeholder = st.empty()

while True:
    try:
        df = yf.download(symbol, period="2d", interval=timeframe, progress=False)
        if not df.empty:
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_200'] = ta.ema(df['Close'], length=200)
            last_row = df.iloc[-1]
            price, rsi, ema_200 = last_row['Close'], last_row['RSI'], last_row['EMA_200']
            
            signal = "NEUTRAL"
            if price > ema_200 and rsi < 35: signal = "🚀 STRONG BUY"
            elif price < ema_200 and rsi > 65: signal = "📉 STRONG SELL"

            with placeholder.container():
                st.metric("Price", f"{price:.5f}")
                st.metric("RSI", f"{rsi:.2f}")
                if signal != "NEUTRAL":
                    st.header(signal)
                    send_telegram_msg(f"🔔 {signal}\nPair: {symbol}\nPrice: {price:.5f}")
    except: pass
    time.sleep(30)
    st.rerun()
