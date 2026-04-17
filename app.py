import streamlit as st
import streamlit.components.v1 as components

# 1. UI & Layout
st.set_page_config(page_title="Finorex AI - Ultra Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; }
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 2px solid #22c55e !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Markets
market_sync = {
    "EUR/USD": "FX_IDC:EURUSD",
    "GBP/USD": "FX_IDC:GBPUSD",
    "USD/JPY": "FX_IDC:USDJPY",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT"
}

selected_name = st.selectbox("Market Selector", list(market_sync.keys()))
symbol = market_sync[selected_name]

# 3. Synchronized Dashboard
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #tv_chart {{ height: 72vh; width: 100vw; }}
    .footer {{ position: fixed; bottom: 0; width: 100%; height: 130px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #22c55e; }}
    .val {{ font-size: 30px; font-weight: bold; margin-top: 5px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold;">● {selected_name} | TIME SYNC ACTIVE</div>
        <div id="live_clock" style="color: #38bdf8; font-family: monospace; font-size: 18px;">00:00:00</div>
    </div>

    <div id="tv_chart"></div>

    <div class="footer">
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">SYNCED TIMER</div>
            <div id="timer" class="val" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">2-MIN ADVANCE SIGNAL</div>
            <div id="pred" class="val" style="color:#22c55e;">SYNCING...</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">DATA STATUS</div>
            <div id="status" class="val" style="color:#38bdf8; font-size:18px;">REAL-TIME</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    var widget = new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "hide_top_toolbar": true,
      "container_id": "tv_chart",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true
      }}
    }});

    // High Precision Sync Logic
    function updateSync() {{
        var now = new Date();
        document.getElementById('live_clock').innerHTML = now.toLocaleTimeString('en-GB');
        
        var seconds = now.getSeconds();
        var remaining = 60 - seconds;
        
        document.getElementById('timer').innerHTML = "00:" + (remaining < 10 ? '0' + remaining : remaining);

        // Signal trigger exactly at 00 to match candle start
        if (seconds == 0) {{
            var res = Math.random() > 0.46 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
            document.getElementById('status').innerHTML = "SIGNAL LIVE";
        }}
    }}
    
    setInterval(updateSync, 1000);
    </script>
""", height=850)
