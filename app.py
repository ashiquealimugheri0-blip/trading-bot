import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Aashique Pro AI - Fixed",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS FOR LOCKING SCREEN & HIDING BARS ---
st.markdown("""
    <style>
    /* Sab margins aur padding khatam */
    .block-container {
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    header, footer, .stDeployButton {
        visibility: hidden;
        height: 0px;
    }
    /* Chart Container ko lock karna */
    .chart-wrapper {
        position: relative;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background-color: #060d14;
    }
    /* Transparent Layer jo dragging ko rokegi */
    /* Agar aapko chart zoom karna ho, toh niche wali 'overlay' class ko comment kar dein */
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 10;
        background: rgba(0,0,0,0); /* Bilkul transparent */
    }
    iframe {
        height: 100vh !important;
        width: 100vw !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FIXED TRADINGVIEW WIDGET ---
def fixed_tradingview_app(symbol):
    # Overlay div dragging ko block karegi
    components.html(f"""
        <div style="position: relative; height: 100vh; width: 100vw; overflow: hidden;">
            <div id="tv_fixed_chart" style="height: 100%; width: 100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
            new TradingView.widget({{
                "autosize": true,
                "symbol": "{symbol}",
                "interval": "1",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#111",
                "enable_publishing": false,
                "hide_top_toolbar": true,      /* Top bar hide kar di taake clean lage */
                "hide_legend": true,
                "save_image": false,
                "container_id": "tv_fixed_chart",
                "lock_assets": true           /* Assets ko lock karne ki koshish */
            }});
            </script>
        </div>
    """, height=1000)

# Render Chart
# Aap apna preferred asset yahan likh sakte hain
fixed_tradingview_app("FX:EURUSD")
