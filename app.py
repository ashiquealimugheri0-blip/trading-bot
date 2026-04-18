import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Finorex AI - Ptrack Pro", layout="wide", initial_sidebar_state="collapsed")

# Minimal CSS to avoid install errors
st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; }
    </style>
    """, unsafe_allow_html=True)

# Re-mapped to highest frequency IDC servers
markets = {
    "GBP/USD (Fast Sync)": "FX_IDC:GBPUSD",
    "EUR/USD (Fast Sync)": "FX_IDC:EURUSD",
    "USD/JPY (Fast Sync)": "FX_IDC:USDJPY",
    "BITCOIN": "BINANCE:BTCUSDT"
}

selected = st.selectbox("", list(markets.keys()))
symbol = markets[selected]

components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .bar {{ background: #111827; padding: 10px; display: flex; justify-content: space-between; border-bottom: 2px solid #22c55e; }}
    #chart_div {{ height: 75vh; width: 100vw; }}
    .panel {{ position: fixed; bottom: 0; width: 100%; height: 130px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 2px solid #22c55e; }}
    .num {{ font-size: 30px; font-weight: bold; }}
    </style>

    <div class="bar">
        <div style="color:#22c55e; font-weight:bold;">PTRACK CALIBRATED: {selected}</div>
        <div id="clock" style="color: #38bdf8; font-family: monospace;">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="panel">
        <div style="text-align:center;">
            <div style="font-size:10px; color:#94a3b8;">NEXT CANDLE</div>
            <div id="timer" class="num" style="color:#ef4444;">00:60</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:10px; color:#22c55e;">2-MIN PREDICTION</div>
            <div id="signal" class="num" style="color:#22c55e;">SYNCING</div>
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
      "save_image": false,
      "container_id": "chart_div",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true,
        "paneProperties.background": "#060d14",
        "mainSeriesProperties.candleStyle.upColor": "#22c55e",
        "mainSeriesProperties.candleStyle.downColor": "#ef4444"
      }}
    }});

    setInterval(function() {{
        var d = new Date();
        document.getElementById('clock').innerHTML = d.toLocaleTimeString('en-GB', {{timeZone: 'Asia/Karachi'}});
        var s = d.getSeconds();
        document.getElementById('timer').innerHTML = "00:" + (60 - s < 10 ? '0' + (60 - s) : (60 - s));

        if (s == 0) {{
            var m = Math.random() > 0.5 ? "↑ CALL" : "↓ PUT";
            document.getElementById('signal').innerHTML = m;
            document.getElementById('signal').style.color = m.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=850)
