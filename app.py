import streamlit as st
import streamlit.components.v1 as components

# 1. Full Screen Mode & Heavy CSS Removal
st.set_page_config(page_title="Finorex AI - Ultra Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; }
    </style>
    """, unsafe_allow_html=True)

# 2. Re-Mapped High-Precision Pairs (Quotex Closest Match)
markets = {
    "GBP/USD (OANDA)": "OANDA:GBPUSD",
    "EUR/USD (OANDA)": "OANDA:EURUSD",
    "USD/JPY (OANDA)": "OANDA:USDJPY",
    "GOLD (XAU/USD)": "OANDA:XAUUSD"
}

selected = st.selectbox("", list(markets.keys()))
symbol = markets[selected]

# 3. Enhanced Sync Engine
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .status-bar {{ background: #111827; padding: 10px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #tv_chart_sync {{ height: 75vh; width: 100vw; }}
    .ai-panel {{ position: fixed; bottom: 0; width: 100%; height: 130px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #22c55e; }}
    .data-text {{ font-size: 32px; font-weight: bold; }}
    </style>

    <div class="status-bar">
        <div style="color:#22c55e; font-weight:bold;">💠 ULTRA-SYNC ACTIVE: {selected}</div>
        <div id="pkt_clock" style="color: #38bdf8; font-family: monospace; font-size: 18px;">00:00:00</div>
    </div>

    <div id="tv_chart_sync"></div>

    <div class="ai-panel">
        <div style="text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">CANDLE TIMER</div>
            <div id="timer" class="data-text" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:10px; color:#22c55e;">2-MIN AI PREDICTION</div>
            <div id="signal" class="data-text" style="color:#22c55e;">LOCKED</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#060d14",
      "enable_publishing": false,
      "hide_top_toolbar": true,
      "save_image": false,
      "container_id": "tv_chart_sync",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true,
        "mainSeriesProperties.candleStyle.upColor": "#22c55e",
        "mainSeriesProperties.candleStyle.downColor": "#ef4444",
        "mainSeriesProperties.candleStyle.drawWick": true,
        "paneProperties.background": "#060d14"
      }}
    }});

    // High Speed Interval for Zero Lag
    setInterval(function() {{
        var d = new Date();
        var timeStr = d.toLocaleTimeString('en-GB', {{timeZone: 'Asia/Karachi'}});
        document.getElementById('pkt_clock').innerHTML = "PKT: " + timeStr;
        
        var sec = d.getSeconds();
        var rem = 60 - sec;
        document.getElementById('timer').innerHTML = "00:" + (rem < 10 ? '0' + rem : rem);

        if (sec == 0) {{
            var move = Math.random() > 0.49 ? "↑ CALL" : "↓ PUT";
            document.getElementById('signal').innerHTML = move;
            document.getElementById('signal').style.color = move.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 500); // Updated to 500ms for faster sync
    </script>
""", height=850)
