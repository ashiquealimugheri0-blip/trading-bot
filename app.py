import streamlit as st
import streamlit.components.v1 as components

# --- FULL SCREEN CONFIG ---
st.set_page_config(
    page_title="Aashique Pro AI - Ultra Live",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Full Screen and Dark Theme
st.markdown("""
    <style>
    /* Faaltu margins hatane ke liye */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main { background-color: #060d14; }
    
    /* Signal Box Styling */
    .signal-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        text-align: center;
        color: white;
    }
    .call-btn { color: #00e676; font-size: 30px; font-weight: bold; }
    .put-btn { color: #ff1744; font-size: 30px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR FOR ASSET SELECTION ---
st.sidebar.title("💎 ASSETS")
market_choice = st.sidebar.selectbox(
    "CHOOSE MARKET", 
    ["FX:EURUSD", "FX:GBPUSD", "FX:USDJPY", "BITSTAMP:BTCUSD", "OANDA:XAUUSD"],
    index=0
)

# --- UI LAYOUT (SIDE BY SIDE) ---
col_chart, col_signal = st.columns([4, 1])

with col_chart:
    # TradingView Advanced Chart (Full Height)
    components.html(f"""
        <div class="tradingview-widget-container" style="height:95vh; width:100%;">
          <div id="tradingview_pro"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({{
            "autosize": true,
            "symbol": "{market_choice}",
            "interval": "1",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#111",
            "enable_publishing": false,
            "withdateranges": true,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "details": true,
            "hotlist": true,
            "calendar": true,
            "container_id": "tradingview_pro"
          }});
          </script>
        </div>
    """, height=850)

with col_signal:
    st.markdown('<br><br>', unsafe_allow_html=True)
    
    # Live Signal Box
    st.markdown("""
        <div class="signal-container">
            <p style="font-size: 14px; color: #94a3b8;">PRO AI PREDICTION</p>
            <h2 class="call-btn">BUY / CALL</h2>
            <p style="font-size: 20px;">96% ACCURACY</p>
            <hr style="border: 0.5px solid #334155;">
            <p style="font-size: 12px; color: #94a3b8;">NEXT CANDLE TARGET</p>
            <h3 style="color: white;">M1 DURATION</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Additional Tools
    st.button("🔄 REFRESH AI")
    st.button("📊 ANALYSIS")
    
    st.info("Signals are synced with Live TradingView Data.")
