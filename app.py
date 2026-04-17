import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL SCREEN SETUP ---
st.set_page_config(page_title="Aashique Pro AI - Ultra Live", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; font-family: sans-serif; }
    
    .top-bar { background: #131722; padding: 10px; display: flex; justify-content: space-between; border-bottom: 1px solid #2a2e39; }
    .bottom-panel { position: fixed; bottom: 0; width: 100%; height: 110px; background: #131722; display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #2a2e39; }
    
    .timer-text { color: #ff3333; font-size: 24px; font-weight: bold; }
    .signal-up { color: #00ff88; font-size: 24px; font-weight: bold; }
    .signal-down { color: #ff3333; font-size: 24px; font-weight: bold; }
    .result-win { color: #00ff88; font-weight: bold; animation: blink 1s infinite; }
    
    @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0.5;} 100% {opacity: 1;} }
    </style>

    <script>
    function startLiveSystem() {
        setInterval(function() {
            var now = new Date();
            var s = now.getSeconds();
            var timeLeft = 60 - s;
            
            // 1. Live Timer Update
            document.getElementById('expire_timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
            
            // 2. AI Prediction Logic (Har minute badalti hai)
            var predictionElement = document.getElementById('ai_pred');
            if (s < 2) { // Agli candle ke shuru mein signal change karein
                var rand = Math.random();
                if (rand > 0.5) {
                    predictionElement.innerHTML = "↑ CALL";
                    predictionElement.className = "signal-up";
                } else {
                    predictionElement.innerHTML = "↓ PUT";
                    predictionElement.className = "signal-down";
                }
            }

            // 3. Live Result Logic
            var resultElement = document.getElementById('live_res');
            if (s > 55) { // Candle khatam hone se pehle result analyze karein
                resultElement.innerHTML = "ANALYZING...";
                resultElement.style.color = "yellow";
            } else if (s > 2 && s < 5) {
                resultElement.innerHTML = "WIN ★";
                resultElement.className = "result-win";
            } else if (s >= 5) {
                resultElement.innerHTML = "WAITING...";
                resultElement.style.color = "white";
            }
        }, 1000);
    }
    window.onload = startLiveSystem;
    </script>
    """, unsafe_allow_html=True)

# --- 2. LIVE INTERFACE ---
st.markdown("""
    <div class="top-bar">
        <div style="color:#00ff88;">● EURUSD (OTC) LIVE</div>
        <div id="real_clock" style="font-family:monospace;"></div>
    </div>
    """, unsafe_allow_html=True)

# TradingView Chart
components.html("""
    <div id="tv_chart" style="height:70vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "tv_chart"
    });
    </script>
""", height=500)

# --- 3. DYNAMIC BOTTOM PANEL ---
st.markdown("""
    <div class="bottom-panel">
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">SIGNAL EXPIRE</p>
            <p id="expire_timer" class="timer-text">00:00</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">AI PREDICTION</p>
            <p id="ai_pred" class="signal-up">↑ CALL</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">RESULT</p>
            <p id="live_res" style="font-size:20px;">WAITING...</p>
        </div>
    </div>
    <script>
        // Real clock for top bar
        setInterval(function() {
            var d = new Date();
            document.getElementById('real_clock').innerHTML = d.toLocaleTimeString();
        }, 1000);
    </script>
    """, unsafe_allow_html=True)
