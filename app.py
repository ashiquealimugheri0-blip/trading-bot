import streamlit as st
import streamlit.components.v1 as components

# --- 1. FULL SCREEN & NO PADDING SETUP ---
st.set_page_config(
    page_title="Aashique Pro AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to force fit everything
st.markdown("""
    <style>
    /* Sab gaps khatam karne ke liye */
    .block-container {
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
        height: 100vh !important;
    }
    /* Streamlit ki faltu bars hide karna */
    header, footer, .stDeployButton {
        visibility: hidden;
        height: 0px;
    }
    /* Body background and scroll prevention */
    body, .stApp {
        background-color: #060d14;
        overflow: hidden !important;
    }
    iframe {
        height: 100vh !important;
        width: 100vw !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ASSET SELECTION ---
# Default asset EUR/USD rakha hai
market = "FX:EURUSD"

# --- 3. TRADINGVIEW ULTRA-FIT WIDGET ---
def tradingview_fit_screen(symbol):
    # '100%' height aur width use ki hai taake mobile par fit ho jaye
    components.html(f"""
        <div class="tradingview-widget-container" style="height:100vh; width:100vw; margin:0; padding:0;">
          <div id="tv_chart_fit" style="height:100%; width:100%;"></div>
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
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tv_chart_fit",
            "library_path": "https://s3.tradingview.com/tv.js"
          }});
          </script>
        </div>
    """, height=1200) # Yeh buffer height hai, CSS isay 100vh par lock kar degi

# UI Execution
tradingview_fit_screen(market)
