import streamlit as st
import streamlit.components.v1 as components

# --- 1. SETTINGS & FULL SCREEN ---
st.set_page_config(page_title="Aashique Pro AI - Live", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; color: white; font-family: 'Inter', sans-serif; }
    
    /* Top Bar with Live Clock */
    .live-header {
        background: #131722;
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #2a2e39;
    }
    .clock-display { color: #00ff88; font-family: monospace; font-size: 18px; font-weight: bold; }

    /* Bottom Signal Panel */
    .bottom-panel {
        position: fixed;
        bottom: 0;
        width: 100%;
        height: 110px;
        background: #131722;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid #2a2e39;
        z-index: 1000;
    }
    .status-dot { height: 10px; width: 10px; background-color: #00ff88; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style>
    
    <script>
    function updateClock() {
        var now = new Date();
        var h = now.getHours();
        var m = now.getMinutes();
        var s = now.getSeconds();
        m = m < 10 ? '0' + m : m;
        s = s < 10 ? '0' + s : s;
        document.getElementById('live_clock').innerHTML = h + ":" + m + ":" + s;
        
        // Candle Countdown (1 min)
        var timeLeft = 60 - s;
        document.getElementById('candle_timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
    }
    setInterval(updateClock, 1000);
    </script>
    """, unsafe_allow_html=True)

# --- 2. LIVE HEADER ---
st.markdown("""
    <div class="live-header">
        <div><span class="status-dot"></span> <b>EURUSD (OTC) LIVE</b></div>
        <div class="clock-display" id="live_clock">00:00:00</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. LIVE TRADINGVIEW (Fastest Server) ---
# Is widget mein interval '1' (1 minute) hai jo live broker se sync hai
components.html("""
    <div id="tv_live" style="height:70vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "autosize": true,
      "symbol": "FX:EURUSD",
      "interval": "1",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "hide_top_toolbar": true,
      "hide_legend": true,
      "container_id": "tv_live"
    });
    </script>
""", height=500)

# --- 4. BOTTOM SIGNAL & COUNTDOWN ---
st.markdown("""
    <div class="bottom-panel">
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">SIGNAL EXPIRE</p>
            <p id="candle_timer" style="color:#ff3333; font-size:22px; font-weight:bold; font-family:monospace;">00:00</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">AI PREDICTION</p>
            <p style="color:#00ff88; font-size:28px; font-weight:bold; margin:0;">↑ CALL</p>
        </div>
        <div style="text-align:center;">
            <p style="margin:0; color:#94a3b8; font-size:12px;">RESULT</p>
            <p style="color:white; font-size:18px;">WAITING...</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
