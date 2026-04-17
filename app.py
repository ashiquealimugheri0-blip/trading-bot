import streamlit as st
import streamlit.components.v1 as components

# --- 1. APP CONFIG (NO PADDING / NO SCROLL) ---
st.set_page_config(page_title="Aashique Pro AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Full Screen Fix */
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { overflow: hidden; background-color: #060d14; }

    /* Top Navigation Bar Style */
    .top-nav {
        background: #131722;
        height: 50px;
        display: flex;
        align-items: center;
        padding-left: 15px;
        border-bottom: 1px solid #2a2e39;
        color: white;
        font-weight: bold;
    }

    /* Bottom Signal Bar Style */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        width: 100%;
        height: 100px;
        background: #131722;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid #2a2e39;
        z-index: 100;
    }
    .signal-text { color: #00ff88; font-size: 24px; font-weight: bold; margin: 0; }
    .timer { color: #ff3333; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TOP NAV BAR ---
st.markdown('<div class="top-nav">💎 EURUSD (OTC) | LIVE ACCOUNT </div>', unsafe_allow_html=True)

# --- 3. FIT-SCREEN CHART ---
# Maine height ko 70% kiya hai taake niche signal bar ki jagah bane
components.html("""
    <div id="chart_container" style="height:70vh; width:100vw;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({
      "container_id": "chart_container",
      "autosize": true,
      "symbol": "FX:EURUSD",
      "interval": "1",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_top_toolbar": true,
      "save_image": false,
      "hide_side_toolbar": true,
      "allow_symbol_change": false
    });
    </script>
""", height=550)

# --- 4. BOTTOM SIGNAL BAR (Finorex Style) ---
st.markdown("""
    <div class="bottom-bar">
        <div>
            <p style="margin:0; color: #94a3b8; font-size: 12px;">NEXT SIGNAL</p>
            <p class="signal-text">⬆ CALL</p>
        </div>
        <div style="text-align: center;">
            <p style="margin:0; color: #94a3b8; font-size: 12px;">TIME LEFT</p>
            <p class="timer">00:42</p>
        </div>
        <div style="text-align: right;">
            <p style="margin:0; color: #94a3b8; font-size: 12px;">ACCURACY</p>
            <p style="color:white; font-weight:bold; margin:0;">98.4%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
