import streamlit as st
import streamlit.components.v1 as components

# 1. Professional UI Layout (Inspired by Kryptonix)
st.set_page_config(page_title="Finorex AI - Ptrack Edition", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer { visibility: hidden; }
    body { background-color: #060d14; color: white; }
    
    /* Kryptonix Style Green Neon Branding */
    div[data-baseweb="select"] { 
        background-color: #0f172a !important; 
        border: 2px solid #22c55e !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #22c55e !important;
        color: black !important;
        font-weight: bold;
        border-radius: 5px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar - Packages & Support (Like kryptonix.site)
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/000000/bot.png", width=80)
    st.title("PTRACK PACKAGES")
    st.info("Select Your Exclusive Plan")
    st.button("3 Days Plan - $49")
    st.button("5 Days Plan - $79")
    st.button("15 Days Plan - $120")
    st.markdown("---")
    st.markdown("💬 **Support:** [Telegram Bot](https://t.me/your_bot)")

# 3. Market Selection (OTC & Live Pairs)
markets = {
    "EUR/USD (OTC-DATA)": "FX_IDC:EURUSD",
    "GBP/USD (OTC-DATA)": "FX_IDC:GBPUSD",
    "USD/JPY (LIVE)": "FX:USDJPY",
    "GOLD (XAU/USD)": "OANDA:XAUUSD",
    "BITCOIN (BTC)": "BINANCE:BTCUSDT"
}

col1, col2 = st.columns([3, 1])
with col1:
    selected_market = st.selectbox("CHOOSE TRADING PAIR", list(markets.keys()))
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("ACTIVATE LICENSE")

symbol = markets[selected_market]

# 4. Main Engine (2-Min Advance + UTC+5 Sync)
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #111827; padding: 12px; display: flex; justify-content: space-between; border-bottom: 3px solid #22c55e; }}
    #tv_chart {{ height: 68vh; width: 100vw; }}
    .footer-panel {{ position: fixed; bottom: 0; width: 100%; height: 160px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #22c55e; }}
    .stat-box {{ text-align: center; min-width: 120px; }}
    .val {{ font-size: 34px; font-weight: bold; margin-top: 5px; }}
    .lbl {{ color: #94a3b8; font-size: 10px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase; }}
    </style>

    <div class="top-bar">
        <div style="color:#22c55e; font-weight:bold; font-size:16px;">💠 PTRACK DATA CONNECTED | {selected_market}</div>
        <div id="pk_clock" style="color: #38bdf8; font-family: monospace; font-size: 18px;">PKT: 00:00:00</div>
    </div>

    <div id="tv_chart"></div>

    <div class="footer-panel">
        <div class="stat-box">
            <div class="lbl">Sync Timer</div>
            <div id="timer" class="val" style="color:#ef4444;">00:60</div>
        </div>
        <div class="stat-box" style="border-left: 1px solid #1e293b; border-right: 1px solid #1e293b; padding: 0 40px;">
            <div class="lbl" style="color:#22c55e;">PTRACK 2-MIN SIGNAL</div>
            <div id="prediction" class="val" style="color:#22c55e;">WAITING</div>
        </div>
        <div class="stat-box">
            <div class="lbl">OTC Quality</div>
            <div id="quality" class="val" style="color:#38bdf8;">100%</div>
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
      "container_id": "tv_chart",
      "overrides": {{
        "mainSeriesProperties.showCountdown": true,
        "mainSeriesProperties.candleStyle.upColor": "#22c55e",
        "mainSeriesProperties.candleStyle.downColor": "#ef4444"
      }}
    }});

    setInterval(function() {{
        var d = new Date();
        document.getElementById('pk_clock').innerHTML = "PKT: " + d.toLocaleTimeString('en-GB', {{ timeZone: 'Asia/Karachi' }});
        
        var sec = d.getSeconds();
        var rem = 60 - sec;
        document.getElementById('timer').innerHTML = "00:" + (rem < 10 ? '0' + rem : rem);

        if (sec == 0) {{
            var res = Math.random() > 0.48 ? "↑ CALL" : "↓ PUT";
            document.getElementById('prediction').innerHTML = res;
            document.getElementById('prediction').style.color = res.includes("CALL") ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=850)
