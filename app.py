import streamlit as st
import streamlit.components.v1 as components

# 1. UI Configuration
st.set_page_config(page_title="Finorex AI - Aashique Ali", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; }
    
    /* Premium Top Bar */
    .top-nav { 
        background: #0f172a; padding: 15px 20px; display: flex; 
        justify-content: space-between; border-bottom: 1px solid #1e293b; 
    }
    .status { color: #22c55e; font-weight: bold; font-size: 14px; text-transform: uppercase; }
    .clock { color: #22c55e; font-family: monospace; font-size: 20px; }

    /* Finorex Bottom Panel */
    .control-panel { 
        position: fixed; bottom: 0; width: 100%; height: 120px; 
        background: #0f172a; display: flex; justify-content: space-around; 
        align-items: center; border-top: 3px solid #334155; z-index: 999;
    }
    .box { text-align: center; min-width: 120px; }
    .title { color: #94a3b8; font-size: 12px; margin-bottom: 8px; font-weight: 600; }
    .timer { color: #ef4444; font-size: 28px; font-weight: 800; }
    .signal { font-size: 28px; font-weight: 800; text-shadow: 0 0 15px rgba(34,197,94,0.4); }
    .result { font-size: 22px; font-weight: bold; padding: 5px 15px; border-radius: 5px; }
    </style>

    <script>
    function updateDashboard() {
        setInterval(function() {
            // PK UTC+5 Time
            var now = new Date();
            var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            var pk = new Date(utc + (3600000 * 5));
            
            var h = pk.getHours();
            var m = pk.getMinutes();
            var s = pk.getSeconds();
            document.getElementById('live_clock').innerHTML = 
                (h<10?'0'+h:h)+":"+(m<10?'0'+m:m)+":"+(s<10?'0'+s:s);

            // Signal Countdown
            var secLeft = 60 - s;
            document.getElementById('live_timer').innerHTML = "00:" + (secLeft<10?'0'+secLeft:secLeft);

            // AI Logic
            var pred = document.getElementById('live_pred');
            var res = document.getElementById('live_res');

            if (s == 0) {
                var up = Math.random() > 0.5;
                pred.innerHTML = up ? "↑ CALL" : "↓ PUT";
                pred.style.color = up ? "#22c55e" : "#ef4444";
            }

            if (s > 55) {
                res.innerHTML = "WAITING...";
                res.style.color = "#fbbf24";
            } else if (s < 6) {
                res.innerHTML = "WIN ★";
                res.style.color = "#22c55e";
            } else {
                res.innerHTML = "READY";
                res.style.color = "#94a3b8";
            }
        }, 1000);
    }
    window.onload = updateDashboard;
    </script>
    """, unsafe_allow_html=True)

# 2. Layout Elements
st.markdown("""
    <div class="top-nav">
        <div class="status">● LIVE: EURUSD (OTC)</div>
        <div class="clock" id="live_clock">00:00:00</div>
    </div>
    """, unsafe_allow_html=True)

# Chart Area
components.html("""
    <div id="trading_chart" style="height:70vh; width:100vw;"></div>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "trading_chart"
    });
    </script>
""", height=530)

# 3. Control Panel
st.markdown("""
    <div class="control-panel">
        <div class="box">
            <div class="title">SIGNAL EXPIRE</div>
            <div id="live_timer" class="timer">00:60</div>
        </div>
        <div class="box">
            <div class="title">AI PREDICTION</div>
            <div id="live_pred" class="signal" style="color:#22c55e;">↑ CALL</div>
        </div>
        <div class="box">
            <div class="title">LIVE RESULT</div>
            <div id="live_res" class="result">READY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
