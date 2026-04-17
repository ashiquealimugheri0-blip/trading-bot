import streamlit as st
import streamlit.components.v1 as components

# Page Setup
st.set_page_config(page_title="Finorex AI - Real-Time Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    .stSelectbox { margin: 10px 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# Exact Live Markets Mapping
live_sync_pairs = {
    "EUR/USD (LIVE)": "FX_IDC:EURUSD",
    "GBP/USD (LIVE)": "FX_IDC:GBPUSD",
    "USD/BRL (LIVE)": "OANDA:USDBRL",
    "USD/BDT (LIVE)": "FX_IDC:USDBDT",
    "USD/INR (LIVE)": "FX_IDC:USDINR",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT"
}

# Market Selector
selected_market = st.selectbox("🎯 MATCH MARKET WITH QUOTEX", list(live_sync_pairs.keys()))
symbol = live_sync_pairs[selected_market]

# Live Chart Component
components.html(f"""
    <div id="tradingview_sync" style="height: 85vh; width: 100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_top_toolbar": true,
      "save_image": false,
      "container_id": "tradingview_sync"
    }});
    </script>
""", height=650)

# Prediction Panel
st.markdown(f"""
    <div style="background:#0f172a; padding:15px; border-radius:10px; border:2px solid #22c55e; margin:10px;">
        <h3 style="color:white; text-align:center; margin:0;">📊 SYNC STATUS: <span style="color:#22c55e;">LIVE</span></h3>
        <p style="color:#94a3b8; text-align:center; font-size:12px;">Ensure Quotex is NOT in OTC mode for exact matching.</p>
    </div>
""", unsafe_allow_html=True)
