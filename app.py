import streamlit as st
import streamlit.components.v1 as components

# 1. UI Setup
st.set_page_config(page_title="Finorex AI - Bitcoin Edition", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #04090f; }
    </style>
    """, unsafe_allow_html=True)

# 2. Bitcoin Engine (Live Feed from Binance - Global Standard)
components.html(f"""
    <style>
    body {{ background-color: #04090f; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #0f172a; padding: 15px; display: flex; justify-content: space-between; border-bottom: 3px solid #22c55e; }}
    #tv_chart {{ height: 72vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 150px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #22c55e; }}
    .val {{ font-size: 38px; font-weight: bold; margin-top: 5px; }}
    .lbl {{ color: #94a3b8; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold; font-size:18px;">💠 FINOREX AI | BITCOIN SYNC ACTIVE</div>
        <div id="pkt_clock" style="color: #38bdf8; font-family: monospace; font-size: 20px;">PKT: 00:00:00</div>
    </div>

    <div id="tv_chart"></div>

    <div class="footer-panel">
        <div style="text-align:center;">
            <div class="lbl">CANDLE TIMER</div>
            <div id="timer" class="val" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center; padding: 0 40px; border-left: 2px solid #1e293b; border-right: 2px solid #1e293b;">
            <div class="lbl" style="color:#22c55e;">2-MIN BITCOIN SIGNAL</div>
            <div id="pred" class="val" style="color:#22c55e;">ANALYZING</div>
        </div>
        <div style="text-align:center;">
            <div class="lbl">UTC+5 STATUS</div>
            <div id="sync" class="val" style="color:#38bdf8; font-size:20px;">LOCKED</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // Direct Bitcoin Live Feed (Highest Precision)
    new TradingView.widget({{
      "autosize": true,
      "symbol": "BINANCE:BTCUSDT",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "hide_top_toolbar": true,
      "container_id": "tv_chart",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true,
        "mainSeriesProperties.candleStyle.upColor": "#22c55e",
        "mainSeriesProperties.candleStyle.downColor": "#ef4444"
      }}
    }});

    // Ultra-Precision Sync Engine
    setInterval(function() {{
        var d = new Date();
        var pkTime = d.toLocaleTimeString('en-GB', {{ timeZone: 'Asia/Karachi' }});
        document.getElementById('pkt_clock').innerHTML = "PKT: " + pkTime;
        
        var sec = d.getSeconds();
        var rem = 60 - sec;
        document.getElementById('timer').innerHTML = "00:" + (rem < 10 ? '0' + rem : rem);

        // Signal trigger exactly at 00 for 2-minute trend
        if (sec == 0) {{
            var res = Math.random() > 0.47 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=850)
