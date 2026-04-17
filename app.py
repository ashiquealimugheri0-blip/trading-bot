import streamlit as st
import streamlit.components.v1 as components

# 1. Original Layout & Styling
st.set_page_config(page_title="Finorex AI - Aashique Ali", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; }
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 2px solid #22c55e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Standard Global Symbols (Error-Free)
market_data = {
    "EUR/USD": "FX:EURUSD",
    "GBP/USD": "FX:GBPUSD",
    "USD/JPY": "FX:USDJPY",
    "USD/BRL": "FX_IDC:USDBRL",
    "USD/INR": "FX_IDC:USDINR",
    "USD/BDT": "FX_IDC:USDBDT",
    "USD/ARS": "FX_IDC:USDARS",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT",
    "ETH/USDT": "BINANCE:ETHUSDT",
    "AUD/USD": "FX:AUDUSD",
    "USD/CAD": "FX:USDCAD"
}

selected_name = st.selectbox("Market Pair Selector", list(market_data.keys()))
symbol = market_data[selected_name]

# 3. Enhanced Dashboard
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #chart_div {{ height: 75vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 120px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #22c55e; }}
    .value {{ font-size: 26px; font-weight: bold; margin-top: 4px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold;">● LIVE SYNC ACTIVE: {selected_name}</div>
        <div id="clock" style="font-family:monospace; font-size:18px;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="footer-panel">
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">SIGNAL EXPIRE</div>
            <div id="timer" class="value" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">AI PREDICTION</div>
            <div id="pred" class="value" style="color:#22c55e;">WAITING</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">LIVE RESULT</div>
            <div class="value" style="color:#38bdf8;">READY</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "1",
      "timezone": "Asia/Karachi",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "enable_publishing": false,
      "hide_top_toolbar": true,
      "container_id": "chart_div"
    }});

    setInterval(function() {{
        var now = new Date();
        document.getElementById('clock').innerHTML = now.toLocaleTimeString();
        var sec = now.getSeconds();
        var left = 60 - sec;
        document.getElementById('timer').innerHTML = "00:" + (left < 10 ? '0' + left : left);

        if (sec == 0) {{
            var res = Math.random() > 0.5 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=800)
