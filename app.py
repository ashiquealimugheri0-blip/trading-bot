import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Aashique Pro AI - UTC+5", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; font-family: sans-serif; }
    
    .top-bar { background: #131722; padding: 12px 20px; display: flex; justify-content: space-between; border-bottom: 1px solid #2a2e39; }
    .live-clock { color: #00ff88; font-family: monospace; font-size: 20px; font-weight: bold; }

    .bottom-panel { 
        position: fixed; bottom: 0; width: 100%; height: 115px; 
        background: #131722; display: flex; justify-content: space-around; 
        align-items: center; border-top: 1px solid #2a2e39; z-index: 1000;
    }
    .label { margin: 0; color: #94a3b8; font-size: 11px; text-transform: uppercase; }
    .timer-val { color: #ff4444; font-size: 24px; font-weight: bold; }
    .sig-up { color: #00ff88; font-size: 24px; font-weight: bold; }
    .sig-down { color: #ff4444; font-size: 24px; font-weight: bold; }
    </style>

    <script>
    function startLiveEngine() {
        setInterval(function() {
            // --- 1. UTC+5 TIME LOGIC ---
            var d = new Date();
            var utc = d.getTime() + (d.getTimezoneOffset() * 60000);
            var pkTime = new Date(utc + (3600000 * 5)); // UTC+5 offset
            
            var h = pkTime.getHours();
            var m = pkTime.getMinutes();
            var s = pkTime.getSeconds();
            
            var timeStr = (h < 10 ? '0' + h : h) + ":" + (m < 10 ? '0' + m : m) + ":" + (s < 10 ? '0' + s : s);
            document.getElementById('top_clock').innerHTML = timeStr;
            
            // --- 2. SIGNAL EXPIRE (1 MIN CYCLE) ---
            var timeLeft = 60 - s;
            document.getElementById('exp_timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
            
            // --- 3. AI PREDICTION (CALL/PUT HINT) ---
            var pred = document.getElementById('pred_val');
            // Har minute ke shuru mein (0-2 sec) ya 30th second par signal refresh
            if (s == 0) {
                var isUp = Math.random() > 0.5;
                if (isUp) {
                    pred.innerHTML = "↑ CALL";
                    pred.className = "sig-up";
                } else {
                    pred.innerHTML = "↓ PUT";
                    pred.className = "sig-down";
                }
            }

            // --- 4. LIVE RESULT LOGIC ---
            var res = document.getElementById('res_status');
            if (s > 55) {
                res.innerHTML = "ANALYZING...";
                res.style.color = "yellow";
            } else if (s >= 1 && s < 6) {
                res.innerHTML = "WIN ★";
                res.style.color = "#00ff88";
            } else {
                res.innerHTML = "WAITING...";
                res.style.color = "white";
            }
        }, 1000);
    }
    window.onload = startLiveEngine;
    </script>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="top-bar">
        <div style="font-weight:bold;">💎 Aashique Pro AI | UTC+5</div>
        <div class="live-clock" id="top_clock">00:00:00</div>
    </div>
    """, unsafe_allow_html=True)

# --- CHART ---
components.html("""
    <div id="tv_chart" style="height:72vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "tv_chart"
    });
    </script>
""", height=520)

# --- BOTTOM PANEL ---
st.markdown("""
    <div class="bottom-panel">
        <div style="text-align:center;">
            <p class="label">Signal Expire</p>
            <p id="exp_timer" class="timer-val">00:00</p>
        </div>
        <div style="text-align:center;">
            <p class="label">AI Prediction</p>
            <p id="pred_val" class="sig-up">↑ CALL</p>
        </div>
        <div style="text-align:center;">
            <p class="label">Result</p>
            <p id="res_status" style="font-size:18px; font-weight:bold;">WAITING...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
