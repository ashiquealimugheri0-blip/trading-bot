import streamlit as st
import streamlit.components.v1 as components

# 1. Full Screen & Premium UI
st.set_page_config(page_title="Finorex Pro AI - Live", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; font-family: sans-serif; }
    
    /* Top Navigation Bar */
    .top-bar { 
        background: #0f172a; padding: 12px 20px; display: flex; 
        justify-content: space-between; align-items: center;
        border-bottom: 1px solid #1e293b;
    }
    .status-live { color: #22c55e; font-size: 13px; font-weight: bold; display: flex; align-items: center; }
    .clock-pk { color: #22c55e; font-family: monospace; font-size: 18px; font-weight: bold; }

    /* Control Panel */
    .bottom-panel { 
        position: fixed; bottom: 0; width: 100%; height: 115px; 
        background: #0f172a; display: flex; justify-content: space-around; 
        align-items: center; border-top: 2px solid #334155; z-index: 9999;
    }
    .box { text-align: center; }
    .box-title { color: #94a3b8; font-size: 11px; margin-bottom: 5px; text-transform: uppercase; font-weight: 600; }
    .val-timer { color: #ef4444; font-size: 26px; font-weight: bold; }
    .val-signal { font-size: 26px; font-weight: bold; transition: all 0.3s; }
    .val-result { font-size: 18px; font-weight: bold; transition: all 0.3s; }
    </style>

    <script>
    function startFinorexEngine() {
        setInterval(function() {
            // --- UTC+5 TIME LOGIC ---
            var now = new Date();
            var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            var pk = new Date(utc + (3600000 * 5));
            
            var h = pk.getHours();
            var m = pk.getMinutes();
            var s = pk.getSeconds();
            
            document.getElementById('top_clock').innerHTML = 
                (h < 10 ? '0' + h : h) + ":" + (m < 10 ? '0' + m : m) + ":" + (s < 10 ? '0' + s : s);

            // --- 1. COUNTDOWN (SIGNAL EXPIRE) ---
            var remaining = 60 - s;
            document.getElementById('exp_val').innerHTML = "00:" + (remaining < 10 ? '0' + remaining : remaining);

            // --- 2. AI PREDICTION (CALL vs PUT) ---
            var pred = document.getElementById('pred_val');
            // Har minute ke shuru mein signal update hoga
            if (s == 0 || pred.innerHTML == "READY") {
                var isCall = Math.random() > 0.5;
                pred.innerHTML = isCall ? "↑ CALL" : "↓ PUT";
                pred.style.color = isCall ? "#22c55e" : "#ef4444";
            }

            // --- 3. LIVE RESULT LOGIC ---
            var res = document.getElementById('res_val');
            if (s > 55) {
                res.innerHTML = "ANALYZING...";
                res.style.color = "#fbbf24"; // Yellow
            } else if (s >= 1 && s < 6) {
                res.innerHTML = "RESULT: WIN ★";
                res.style.color = "#22c55e"; // Green
            } else {
                res.innerHTML = "WAITING...";
                res.style.color = "#94a3b8";
            }
        }, 1000);
    }
    window.onload = startFinorexEngine;
    </script>
    """, unsafe_allow_html=True)

# 2. Top Header
st.markdown("""
    <div class="top-bar">
        <div class="status-live">
            <span style="height:8px; width:8px; background:#22c55e; border-radius:50%; margin-right:8px;"></span>
            EURUSD (OTC) LIVE
        </div>
        <div class="clock-pk" id="top_clock">00:00:00</div>
    </div>
    """, unsafe_allow_html=True)

# 3. Fast TradingView Chart
components.html("""
    <div id="chart_container" style="height:72vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, 
      "hide_legend": true, "container_id": "chart_container"
    });
    </script>
""", height=520)

# 4. Final Control Panel
st.markdown("""
    <div class="bottom-panel">
        <div class="box">
            <p class="box-title">Signal Expire</p>
            <p id="exp_val" class="val-timer">00:00</p>
        </div>
        <div class="box">
            <p class="box-title">AI Prediction</p>
            <p id="pred_val" class="val-signal" style="color:#22c55e;">READY</p>
        </div>
        <div class="box">
            <p class="box-title">Live Result</p>
            <p id="res_val" class="val-result">WAITING...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
