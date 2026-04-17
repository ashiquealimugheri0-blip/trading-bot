import streamlit as st
import yfinance as yf
import pandas_ta as ta
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Quotex Pro AI", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    [data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- Telegram Settings ---
TOKEN = "8192017754:AAEOJEsKSPgBYNyFVB7d65neaVvyJnx13z8"
CHAT_ID = "7017764790"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    try:
        requests.get(url, timeout=5)
    except:
        pass

st.title("📊 Quotex Pro AI Dashboard")

# Sidebar settings
symbol = st.sidebar.text_input("Asset Symbol", "EURUSD=X")
timeframe = st.sidebar.selectbox("Timeframe", ("1m", "5m", "15m"), index=0)

# Create a placeholder for the live dashboard
dashboard = st.empty()

while True:
    try:
        # Step 1: Download Data
        # 'auto_adjust=True' and picking only 'Close' ensures we don't get a MultiIndex Series
        data = yf.download(symbol, period="1d", interval=timeframe, progress=False, auto_adjust=True)
        
        if not data.empty and len(data) > 20:
            df = data.copy()
            
            # Handling potential MultiIndex or duplicate columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Step 2: Calculate Indicators
            df['RSI'] = ta.rsi(df['Close'], length=14)
            df['EMA_200'] = ta.ema(df['Close'], length=200)
            
            # Step 3: Extract Latest Values Safely
            # Using .item() or float() on the last element of the series
            current_price = float(df['Close'].iloc[-1])
            current_rsi = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 50.0
            current_ema = float(df['EMA_200'].iloc[-1]) if not pd.isna(df['EMA_200'].iloc[-1]) else current_price

            # Step 4: Update Dashboard UI
            with dashboard.container():
                cols = st.columns(3)
                cols[0].metric("Price", f"{current_price:.5f}")
                cols[1].metric("RSI (14)", f"{current_rsi:.2f}")
                cols[2].metric("EMA 200", f"{current_ema:.5f}")

                # Candlestick Chart
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'],
                    increasing_line_color='#00b97a', 
                    decreasing_line_color='#ff3b3b'
                )])
                fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)

                # Signal Logic
                signal_text = "SCANNING MARKET..."
                bg_color = "#161b22"
                
                if current_price > current_ema and current_rsi < 35:
                    signal_text = "🟢 BUY SIGNAL (CALL)"
                    bg_color = "#00b97a"
                    send_telegram_msg(f"🚀 BUY: {symbol} @ {current_price}")
                elif current_price < current_ema and current_rsi > 65:
                    signal_text = "🔴 SELL SIGNAL (PUT)"
                    bg_color = "#ff3b3b"
                    send_telegram_msg(f"📉 SELL: {symbol} @ {current_price}")

                st.markdown(f"""
                    <div style='text-align: center; background-color: {bg_color}; padding: 25px; border-radius: 15px; font-size: 30px; font-weight: bold;'>
                        {signal_text}
                    </div>
                """, unsafe_allow_html=True)
                
        else:
            st.warning("🔄 Fetching data... Please wait.")

    except Exception as e:
        st.error(f"⚠️ Connection Pause: Reconnecting in 60s...")
        # Rate limit se bachne ke liye lamba intezar
        time.sleep(60)
        continue

    # Refresh every 60 seconds to stay safe from Yahoo Finance blocking
    time.sleep(60)
