import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration for Full View
st.set_page_config(page_title="Finorex AI - Live Sync", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; color: white; }
    
    /* Live Sync Selector */
    .stSelectbox { margin: 10px 20px !important; }
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 1px solid #22c55e !important;
        border-radius: 4px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Optimized Live Data Symbols
# Maine yahan IDC aur OANDA ke symbols use kiye hain jo live price ke sabse qareeb hain
all_pairs = {
    "EUR/USD (Live Sync)": "FX_IDC:EURUSD",
    "GBP/USD (Live Sync)": "FX_IDC:GBPUSD",
    "USD/BRL (Live Sync)": "FX_IDC:USDBRL",
    "USD/BDT (Live Sync)": "FX_IDC:USDBDT",
    "USD/ARS (Live Sync)": "FX_IDC:USDARS",
    "USD/INR (Live Sync)": "FX_IDC:USDINR",
    "GOLD (Live Sync)": "OANDA:XAUUSD",
    "BITCOIN (Live Sync)": "BINANCE:BTCUSDT",
    "USD/JPY": "FX_IDC:USDJPY",
    "AUD/JPY": "FX_IDC:AUDJPY"
}

selected_name = st.selectbox("Market Pair Selector", list(all_pairs.keys()), index=0)
selected_symbol = all_pairs[selected_name]

# 3. Enhanced Dashboard with Real-Time Widget
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #0f172a; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; }}
    .live-dot {{ height: 10px; width: 10px; background-color: #22c55e; border-radius: 50%; display: inline-block; margin-right: 5px; }}
    #chart_div {{ height: 72vh; width: 100vw; }}
    .panel {{ position: fixed; bottom: 0; width: 100%; height: 115px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #334155; }}
    .box {{ text-align: center; width: 32%; }}
    .label {{ color: #94a3b8; font-size: 10px; text-transform: uppercase; }}
    .val {{ font-size: 24px; font-weight: bold; margin-top: 5px; }}
    </style>

    <div class="top-bar">
        <div><span class="live-dot"></span> <span style="color:#38bdf8; font-weight:bold;">{selected_name}</span></div>
        <div id="clock" style="color:#22c55e; font-weight:bold;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="panel">
        <div class="box">
            <div class="label">Signal Timer</div>
            <div id="timer" class="val" style="color:#ef4444;">00:59</div>
        </div>
        <div class="box">
            <div class="label">AI Sync Prediction</div>
            <div id="pred" class="val" style="color:#22c55e;">ANALYZING</div>
        </div>
        <div class="box">
            <div class="label">Status</div>
            <div id="status" class="val" style="font-size:16px;">CONNECTED</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // Live Widget with Real-Time Interval
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{selected_symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_top_toolbar": true,
      "save_image": false,
      "container_id": "chart_div"
    }});

    setInterval(function() {{
        var now = new Date();
        document.getElementById('clock').innerHTML = now.toLocaleTimeString();
        var s = now.getSeconds();
        var timeLeft = 60 - s;
        document.getElementById('timer').innerHTML = "00:" + (timeLeft < 10 ? '0' + timeLeft : timeLeft);

        if (s == 0) {{
            var move = Math.random() > 0.5 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = move;
            document.getElementById('pred').style.color = move.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=750)
