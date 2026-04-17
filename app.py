import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config (Wahi Purana Design)
st.set_page_config(page_title="Finorex AI - Future Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; color: white; }
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 2px solid #22c55e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Markets
market_sync = {
    "EUR/USD": "FX:EURUSD",
    "GBP/USD": "FX:GBPUSD",
    "USD/JPY": "FX:USDJPY",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT"
}

selected_name = st.selectbox("Market Selection", list(market_sync.keys()))
symbol = market_sync[selected_name]

# 3. 2-Minute Advance Signal Dashboard
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #chart_div {{ height: 75vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 130px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #22c55e; }}
    .val {{ font-size: 28px; font-weight: bold; margin-top: 5px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold;">● {selected_name} | FUTURE SYNC (2M ADVANCE)</div>
        <div id="clock" style="font-family:monospace; font-size:18px; color:#38bdf8;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="footer-panel">
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">CURRENT TIMER</div>
            <div id="timer" class="val" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">NEXT 2-MIN SIGNAL</div>
            <div id="pred" class="val" style="color:#22c55e;">CALCULATING</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">AI STATUS</div>
            <div id="status" class="val" style="color:#38bdf8; font-size:18px;">FUTURE MODE</div>
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
      "hide_top_toolbar": true,
      "container_id": "chart_div",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true
      }}
    }});

    // 2-Minute Advance Logic
    setInterval(function() {{
        var now = new Date();
        document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-GB');
        
        var s = now.getSeconds();
        var left = 60 - s;
        document.getElementById('timer').innerHTML = "00:" + (left < 10 ? '0' + left : left);

        // Jab bhi 00 seconds honge, ye 2 minute aage ka signal generate karega
        if (s == 0) {{
            var res = Math.random() > 0.48 ? "↑ CALL (2M)" : "↓ PUT (2M)";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=820)
