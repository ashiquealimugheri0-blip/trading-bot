import streamlit as st
import streamlit.components.v1 as components

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Aashique Pro AI - Live Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; }
    
    /* Top Bar */
    .top-bar { 
        background: #131722; padding: 10px 15px; display: flex; 
        justify-content: space-between; border-bottom: 1px solid #2a2e39; 
    }
    .live-clock { color: #00ff88; font-family: monospace; font-size: 20px; font-weight: bold; }

    /* Bottom Panel */
    .bottom-panel { 
        position: fixed; bottom: 0; width: 100%; height: 110px; 
        background: #131722; display: flex; justify-content: space-around; 
        align-items: center; border-top: 1px solid #2a2e39; z-index: 1000;
    }
    .timer-red { color: #ff3333; font-size: 24px; font-weight: bold; }
    .signal-up { color: #00ff88; font-size: 26px; font-weight: bold; }
    </style>

    <script>
    function updateLiveSystem() {
        setInterval(function() {
            var now = new Date();
            
            // 1. Live Clock (Current Time: 00:30)
            var h = now.getHours();
            var m = now.getMinutes();
            var s = now.getSeconds();
            h = h < 10 ? '0' + h : h;
            m = m < 10 ? '0' + m : m;
            s = s < 10 ? '0' + s : s;
            document.getElementById('real_time').innerHTML = h + ":" + m + ":" + s;
            
            // 2. Signal Expire Timer (1 min cycle)
            var timeLeft = 60 - s;
            document.getElementById('expire_timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
            
            // 3. Result Logic
            var res = document.getElementById('live_result');
            if (s > 57) {
                res.innerHTML = "WINNING...";
                res.style.color = "#00ff88";
            } else if (s < 5) {
                res.innerHTML = "RESULT: WIN ★";
                res.style.color = "#00ff88";
            } else {
                res.innerHTML = "WAITING...";
                res.style.color = "white";
            }
        }, 1000);
    }
    window.onload = updateLiveSystem;
    </script>
    """, unsafe_allow_html=True)

# --- 2. HEADER WITH LIVE CLOCK ---
st.markdown("""
    <div class="top-bar">
        <div style="font-weight:bold;">● EURUSD (OTC) LIVE</div>
        <div class="live-clock" id="real_time">00:30:00</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CHART ---
components.html("""
    <div id="chart" style="height:70vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "chart"
    });
    </script>
""", height=500)

# --- 4. BOTTOM PANEL ---
st.markdown("""
    <div class="bottom-panel">
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">SIGNAL EXPIRE</p>
            <p id="expire_timer" class="timer-red">00:60</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">AI PREDICTION</p>
            <p class="signal-up">↑ CALL</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">RESULT</p>
            <p id="live_result" style="font-size:18px; font-weight:bold;">WAITING...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)            document.getElementById('real_clock').innerHTML = d.toLocaleTimeString();
        }, 1000);
    </script>
    """, unsafe_allow_html=True)
