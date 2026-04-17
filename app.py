import streamlit as st
import streamlit.components.v1 as components

# --- 1. PAGE CONFIG (NO PADDING) ---
st.set_page_config(
    page_title="Aashique Pro AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED CSS FOR FULL SCREEN ---
st.markdown("""
    <style>
    /* Sab margins aur padding khatam karne ke liye */
    .block-container {
        padding: 0px !important;
        margin: 0px !important;
        max-width: 100% !important;
    }
    iframe {
        border-radius: 0px !important;
    }
    /* Streamlit ke default menu aur footer ko hide karne ke liye */
    header, footer, .stDeployButton {
        visibility: hidden;
        height: 0px;
    }
    /* Mobile par scroll bar khatam karne ke liye */
    body {
        overflow: hidden;
        background-color: #060d14;
    }
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MARKET SELECTION (SIDEBAR) ---
# Swipe karke ya top arrow se market change kar sakte hain
market = st.sidebar.selectbox(
    "CHOOSE ASSET", 
    ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD"],
    index=0
)

# --- 4. TRADINGVIEW FULL SCREEN WIDGET ---
# Height ko '100vh' (View Height) par set kiya hai taake mobile screen par fit ho
def tradingview_full_app(symbol):
    components.html(f"""
        <div class="tradingview-widget-container" style="height:100vh; width:100vw; margin:0; padding:0;">
          <div id="tv_chart" style="height:100%; width:100%;"></div>
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
            "container_id": "tv_chart"
          }});
          </script>
        </div>
    """, height=1000) # Desktop height, mobile par ye auto set ho jayega

# UI Render
tradingview_full_app(market)
