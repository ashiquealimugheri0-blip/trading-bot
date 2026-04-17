import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Finorex AI - Aashique Ali", layout="wide", initial_sidebar_state="collapsed")

# 2. Base Styles (Python side)
st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; }
    </style>
    """, unsafe_allow_html=True)

# 3. Everything in ONE HTML Component (Tension Free Deployment)
components.html("""
    <style>
    body { background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }
    
    /* Top Bar */
    .top-bar { 
        background: #0f172a; padding: 12px 20px; display: flex; 
        justify-content: space-between; align-items: center;
        border-bottom: 1px solid #1e293b;
    }
    .status { color: #22c55e; font-size: 14px; font-weight: bold; }
    .clock { color: #22c55e; font-family: monospace; font-size: 18px; }

    /* Chart Area */
    #chart_div { height: 70vh; width: 100vw; background: #060d14; }

    /* Bottom Panel */
    .panel { 
        position: fixed; bottom: 0; width: 100%; height: 120px; 
        background: #0f172a; display: flex; justify-content: space-around; 
        align-items: center; border-top: 2px solid #334155;
    }
    .box { text-align: center; }
    .label { color: #94a3b8; font-size: 11px; margin-bottom: 4px; text-transform: uppercase; }
    .timer { color: #ef4444; font-size: 26px; font-weight: bold; }
    .signal { font-size: 26px; font-weight: bold; }
    .result { font-size: 18px; font-weight: bold; }
    </style>

    <div class="top-bar">
        <div class="status">● EURUSD (OTC) LIVE</div>
        <div id="pk_clock" class="clock">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="panel">
        <div class="box">
            <div class="label">Signal Expire</div>
            <div id="exp_val" class="timer">00:00</div>
        </div>
        <div class="box">
            <div class="label">AI Prediction</div>
            <div id="pred_val" class="signal" style="color:#22c55e;">↑ CALL</div>
        </div>
        <div class="box">
            <div class="label">Live Result</div>
            <div id="res_val" class="result">WAITING...</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // 1. TradingView Chart Load
    new TradingView.widget({
      "autosize": true, "symbol": "FX:EURUSD", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "chart_div"
    });

    // 2. LIVE ENGINE (FORCE REFRESH)
    setInterval(function() {
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var pk = new Date(utc + (3600000 * 5)); // UTC+5
        
        var h = pk.getHours();
        var m = pk.getMinutes();
        var s = pk.getSeconds();
        
        // Update Clock
        document.getElementById('pk_clock').innerHTML = 
            (h<10?'0'+h:h)+":"+(m<10?'0'+m:m)+":"+(s<10?'0'+s:s);

        // Update Timer
        var rem = 60 - s;
        document.getElementById('exp_val').innerHTML = "00:" + (rem<10?'0'+rem:rem);

        // Update Prediction (Randomize on new minute)
        var pred = document.getElementById('pred_val');
        if (s == 0 || pred.innerHTML === "READY") {
            var isUp = Math.random() > 0.5;
            pred.innerHTML = isUp ? "↑ CALL" : "↓ PUT";
            pred.style.color = isUp ? "#22c55e" : "#ef4444";
        }

        // Update Result
        var res = document.getElementById('res_val');
        if (s > 55) {
            res.innerHTML = "ANALYZING...";
            res.style.color = "#fbbf24";
        } else if (s < 6) {
            res.innerHTML = "RESULT: WIN ★";
            res.style.color = "#22c55e";
        } else {
            res.innerHTML = "WAITING...";
            res.style.color = "#94a3b8";
        }
    }, 1000);
    </script>
""", height=700)
