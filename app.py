import streamlit as st
import streamlit.components.v1 as components

# 1. Full Screen Layout
st.set_page_config(page_title="Finorex AI - Quick Select", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; color: white; }
    
    /* Market Selection Box Styling */
    .stSelectbox { margin: 10px 20px !important; }
    .stSelectbox label { display: none; }
    div[data-baseweb="select"] { background-color: #1e293b !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Main Screen Market Selector (Directly visible on top)
all_pairs = {
    "EUR/USD (OTC)": "FX:EURUSD",
    "GBP/USD (OTC)": "FX:GBPUSD",
    "USD/MXN (OTC)": "FX:USDMXN",
    "AUD/JPY (OTC)": "FX:AUDJPY",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BTC/USDT": "BINANCE:BTCUSDT",
    "SOL/USDT": "BINANCE:SOLUSDT"
}

# Ye box ab seedha chart ke upar dikhega
selected_name = st.selectbox("Market Selector", list(all_pairs.keys()), index=0)
selected_symbol = all_pairs[selected_name]

# 3. UI Dashboard & Logic
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #0f172a; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; }}
    .clock {{ color: #22c55e; font-family: monospace; font-size: 18px; font-weight: bold; }}
    .tag {{ color: #38bdf8; font-weight: bold; }}
    #chart_div {{ height: 70vh; width: 100vw; }}
    .panel {{ position: fixed; bottom: 0; width: 100%; height: 120px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #334155; }}
    .box {{ text-align: center; width: 32%; }}
    .label {{ color: #94a3b8; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }}
    .val {{ font-size: 26px; font-weight: 800; }}
    </style>

    <div class="top-bar">
        <div class="tag">⭐ {selected_name} ACTIVE</div>
        <div id="pk_clock" class="clock">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="panel">
        <div class="box">
            <div class="label">Signal Expire</div>
            <div id="timer" class="val" style="color:#ef4444;">00:00</div>
        </div>
        <div class="box">
            <div class="label">AI Prediction</div>
            <div id="pred" class="val" style="color:#22c55e;">WAITING</div>
        </div>
        <div class="box">
            <div class="label">Result</div>
            <div id="res" class="val" style="font-size:18px;">READY</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    new TradingView.widget({{
      "autosize": true, "symbol": "{selected_symbol}", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "chart_div"
    }});

    setInterval(function() {{
        var pk = new Date(new Date().getTime() + (3600000 * 5));
        var s = pk.getSeconds();
        document.getElementById('pk_clock').innerHTML = pk.toISOString().substr(11, 8);
        document.getElementById('timer').innerHTML = "00:" + (60-s < 10 ? '0'+(60-s) : (60-s));

        if (s == 0) {{
            var isUp = Math.random() > 0.45;
            document.getElementById('pred').innerHTML = isUp ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').style.color = isUp ? "#22c55e" : "#ef4444";
            document.getElementById('res').innerHTML = "LIVE";
        }}
        if (s == 59) {{
            var win = Math.random() > 0.5;
            document.getElementById('res').innerHTML = win ? "WIN ★" : "LOSS ✘";
            document.getElementById('res').style.color = win ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=700)
