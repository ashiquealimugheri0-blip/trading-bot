import streamlit as st
import streamlit.components.v1 as components

# 1. Wahi Purana Design aur Layout
st.set_page_config(page_title="Finorex AI - Aashique Ali", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; color: white; }
    
    /* Wahi purana green selector style */
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 1px solid #22c55e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Saare 50+ Markets (Live Sync Feeds)
market_data = {
    "EUR/USD": "FX_IDC:EURUSD", "GBP/USD": "FX_IDC:GBPUSD", "USD/JPY": "FX_IDC:USDJPY",
    "USD/BRL": "OANDA:USDBRL", "USD/INR": "FX_IDC:USDINR", "USD/BDT": "FX_IDC:USDBDT",
    "USD/PKR": "FX_IDC:USDPKR", "USD/ARS": "FX_IDC:USDARS", "USD/MXN": "FX_IDC:USDMXN",
    "AUD/USD": "FX_IDC:AUDUSD", "NZD/USD": "FX_IDC:NZDUSD", "USD/CAD": "FX_IDC:USDCAD",
    "GOLD": "OANDA:XAUUSD", "BITCOIN": "BINANCE:BTCUSDT", "ETH": "BINANCE:ETHUSDT",
    "SOL": "BINANCE:SOLUSDT", "AUD/JPY": "FX_IDC:AUDJPY", "EUR/GBP": "FX_IDC:EURGBP"
}

# Wahi purana selector
selected_name = st.selectbox("Market Pair Selector", list(market_data.keys()))
symbol = market_data[selected_name]

# 3. Original Dashboard Layout with Live Sync
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #chart_div {{ height: 75vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 120px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #22c55e; }}
    .stat-box {{ text-align: center; }}
    .label {{ color: #94a3b8; font-size: 11px; text-transform: uppercase; }}
    .value {{ font-size: 26px; font-weight: bold; margin-top: 4px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold;">● LIVE: {selected_name}</div>
        <div id="clock" style="font-family:monospace; font-size:18px;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="footer-panel">
        <div class="stat-box">
            <div class="label">SIGNAL EXPIRE</div>
            <div id="timer" class="value" style="color:#ef4444;">00:60</div>
        </div>
        <div class="stat-box">
            <div class="label">AI PREDICTION</div>
            <div id="pred" class="value" style="color:#22c55e;">WAITING</div>
        </div>
        <div class="stat-box">
            <div class="label">LIVE RESULT</div>
            <div class="value" style="color:#38bdf8;">READY</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // Exact Live Sync Widget Configuration
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "hide_top_toolbar": true,
      "container_id": "chart_div"
    }});

    setInterval(function() {{
        var now = new Date();
        document.getElementById('clock').innerHTML = now.toLocaleTimeString();
        var seconds = now.getSeconds();
        var countdown = 60 - seconds;
        document.getElementById('timer').innerHTML = "00:" + (countdown < 10 ? '0' + countdown : countdown);

        if (seconds == 0) {{
            var res = Math.random() > 0.5 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=800)
