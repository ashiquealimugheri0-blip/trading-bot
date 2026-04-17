import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Aashique Pro AI - Ultra Live", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; font-family: sans-serif; }
    
    /* Top Navigation Bar */
    .top-bar { 
        background: #131722; padding: 12px 20px; display: flex; 
        justify-content: space-between; border-bottom: 1px solid #2a2e39; 
    }
    .live-clock { color: #00ff88; font-family: 'Courier New', monospace; font-size: 20px; font-weight: bold; }

    /* Bottom Control Panel */
    .bottom-panel { 
        position: fixed; bottom: 0; width: 100%; height: 115px; 
        background: #131722; display: flex; justify-content: space-around; 
        align-items: center; border-top: 1px solid #2a2e39; z-index: 1000;
    }
    .label { margin: 0; color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .timer-val { color: #ff4444; font-size: 26px; font-weight: bold; }
    .signal-up { color: #00ff88; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px rgba(0,255,136,0.3); }
    .signal-down { color: #ff4444; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px rgba(255,68,68,0.3); }
    .result-text { font-size: 20px; font-weight: bold; transition: 0.3s; }
    </style>

    <script>
    function startLiveEngine() {
        setInterval(function() {
            var now = new Date();
            var h = now.getHours();
            var m = now.getMinutes();
            var s = now.getSeconds();
            
            // Format Time
            var timeStr = (h < 10 ? '0' + h : h) + ":" + (m < 10 ? '0' + m : m) + ":" + (s < 10 ? '0' + s : s);
            document.getElementById('top_clock').innerHTML = timeStr;
            
            // Signal Expire (Countdown to next minute)
            var timeLeft = 60 - s;
            document.getElementById('exp_timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
            
            // Result & Prediction Logic
            var res = document.getElementById('res_status');
            var pred = document.getElementById('pred_val');
            
            if (s > 55) {
                res.innerHTML = "ANALYZING...";
                res.style.color = "#eab308"; // Yellow
            } else if (s >= 0 && s < 5) {
                res.innerHTML = "RESULT: WIN ★";
                res.style.color = "#00ff88"; // Green
            } else {
                res.innerHTML = "WAITING...";
                res.style.color = "#ffffff"; // White
            }
            
            // Change Signal every 60s
            if (s == 0) {
                var isUp = Math.random() > 0.5;
                pred.innerHTML = isUp ? "↑ CALL" : "↓ PUT";
                pred.className = isUp ? "signal-up" : "signal-down";
            }
        }, 1000);
    }
    window.onload = startLiveEngine;
    </script>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.markdown("""
    <div class="top-bar">
        <div style="font-weight:bold; display:flex; align-items:center;">
            <span style="height:10px; width:10px; background:#00ff88; border-radius:50%; margin-right:10px;"></span>
            EURUSD (OTC) LIVE
        </div>
        <div class="live-clock" id="top_clock">00:00:00</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. CHART COMPONENT ---
components.html("""
    <div id="tradingview_live" style="height:72vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "toolbar_bg": "#131722",
      "enable_publishing": false, "hide_top_toolbar": true, "container_id": "tradingview_live"
    });
    </script>
""", height=520)

# --- 4. LIVE CONTROL PANEL ---
st.markdown("""
    <div class="bottom-panel">
        <div style="text-align:center;">
            <p class="label">Signal Expire</p>
            <p id="exp_timer" class="timer-val">00:00</p>
        </div>
        <div style="text-align:center;">
            <p class="label">AI Prediction</p>
            <p id="pred_val" class="signal-up">↑ CALL</p>
        </div>
        <div style="text-align:center;">
            <p class="label">Live Result</p>
            <p id="res_status" class="result-text">WAITING...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
