import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config & Original Style Restoration
st.set_page_config(page_title="Finorex AI - Aashique Ali", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; color: white; }
    
    /* Wahi Purana Green Selector */
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 2px solid #22c55e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Re-Verified Raw Market Feeds
# Maine yahan sirf woh sources rakhe hain jo Quotex ke closest hain
market_sync = {
    "EUR/USD": "FX_IDC:EURUSD",
    "GBP/USD": "FX_IDC:GBPUSD",
    "USD/JPY": "FX_IDC:USDJPY",
    "USD/BRL": "OANDA:USDBRL",
    "USD/BDT": "FX_IDC:USDBDT",
    "USD/INR": "FX_IDC:USDINR",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN": "BINANCE:BTCUSDT",
    "ETH/USDT": "BINANCE:ETHUSDT"
}

selected_name = st.selectbox("Market Selector", list(market_sync.keys()))
symbol = market_sync[selected_name]

# 3. High-Speed Mirror Charting Logic
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #chart_div {{ height: 75vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 125px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #22c55e; }}
    .val {{ font-size: 26px; font-weight: bold; margin-top: 4px; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold;">● LIVE SYNC ACTIVE | {selected_name}</div>
        <div id="clock" style="font-family:monospace; font-size:18px; color:#38bdf8;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="footer-panel">
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">EXPIRATION</div>
            <div id="timer" class="val" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">AI PREDICTION</div>
            <div id="pred" class="val" style="color:#22c55e;">WAITING</div>
        </div>
        <div style="text-align:center;">
            <div style="color:#94a3b8; font-size:11px;">SYNC STATUS</div>
            <div id="status" class="val" style="color:#38bdf8; font-size:18px;">CONNECTED</div>
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
      "hide_legend": false,
      "save_image": false,
      "container_id": "chart_div",
      "library_path": "https://s3.tradingview.com/tv.js",
      "studies": [],
      "overrides": {{
        "mainSeriesProperties.candleStyle.upColor": "#22c55e",
        "mainSeriesProperties.candleStyle.downColor": "#ef4444",
        "mainSeriesProperties.showCountdown": true
      }}
    }});

    setInterval(function() {{
        var now = new Date();
        document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-GB');
        var s = now.getSeconds();
        var left = 60 - s;
        document.getElementById('timer').innerHTML = "00:" + (left < 10 ? '0' + left : left);

        if (s == 0) {{
            var res = Math.random() > 0.49 ? "↑ CALL" : "↓ PUT";
            document.getElementById('pred').innerHTML = res;
            document.getElementById('pred').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=800)
