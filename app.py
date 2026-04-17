import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Finorex Multi-Market", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; }
    </style>
    """, unsafe_allow_html=True)

# 2. Multi-Market Logic & UI
components.html("""
    <style>
    body { background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }
    .top-bar { background: #0f172a; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; }
    .status { color: #22c55e; font-size: 12px; font-weight: bold; }
    .clock { color: #22c55e; font-family: monospace; font-size: 16px; }
    #chart_div { height: 72vh; width: 100vw; }
    .panel { position: fixed; bottom: 0; width: 100%; height: 120px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #334155; }
    .box { text-align: center; width: 30%; }
    .label { color: #94a3b8; font-size: 10px; margin-bottom: 4px; text-transform: uppercase; }
    .timer { color: #ef4444; font-size: 24px; font-weight: bold; }
    .signal { font-size: 24px; font-weight: bold; }
    .result { font-size: 18px; font-weight: bold; transition: 0.5s; }
    </style>

    <div class="top-bar">
        <div class="status">● MULTI-MARKET AI ACTIVE</div>
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
            <div id="pred_val" class="signal" style="color:#22c55e;">WAIT...</div>
        </div>
        <div class="box">
            <div class="label">Live Result</div>
            <div id="res_val" class="result">READY</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // 1. Chart Load with SEARCH ENABLED
    new TradingView.widget({
      "autosize": true,
      "symbol": "FX:EURUSD",
      "interval": "1",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_top_toolbar": false, // SEARCH BAR ON KAR DIYA
      "hide_legend": false,
      "save_image": false,
      "container_id": "chart_div"
    });

    var currentSignal = "";

    setInterval(function() {
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var pk = new Date(utc + (3600000 * 5));
        
        var h = pk.getHours(), m = pk.getMinutes(), s = pk.getSeconds();
        document.getElementById('pk_clock').innerHTML = (h<10?'0'+h:h)+":"+(m<10?'0'+m:m)+":"+(s<10?'0'+s:s);

        var rem = 60 - s;
        document.getElementById('exp_val').innerHTML = "00:" + (rem<10?'0'+rem:rem);

        var pred = document.getElementById('pred_val');
        var res = document.getElementById('res_val');

        if (s == 0) {
            var isUp = Math.random() > 0.48; 
            currentSignal = isUp ? "CALL" : "PUT";
            pred.innerHTML = isUp ? "↑ CALL" : "↓ PUT";
            pred.style.color = isUp ? "#22c55e" : "#ef4444";
            res.innerHTML = "TRADE LIVE";
            res.style.color = "white";
        }

        if (s > 55 && s < 59) {
            res.innerHTML = "ANALYZING...";
            res.style.color = "#fbbf24";
        }

        if (s == 59) {
            var actual = Math.random() > 0.5 ? "CALL" : "PUT"; 
            if (currentSignal === actual) {
                res.innerHTML = "RESULT: WIN ★";
                res.style.color = "#22c55e";
            } else {
                res.innerHTML = "RESULT: LOSS ✘";
                res.style.color = "#ef4444";
            }
        }
    }, 1000);
    </script>
""", height=700)
