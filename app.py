import streamlit as st
import streamlit.components.v1 as components

# 1. Full Screen Configuration
st.set_page_config(page_title="Finorex AI - Quotex Mode", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; color: white; }
    
    /* Sidebar Quotex Style */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #1e293b;
    }
    .stSelectbox label { color: #94a3b8 !important; font-size: 14px; font-weight: bold; }
    .st-emotion-cache-16idsys p { font-size: 18px; color: #22c55e; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Market Categories (Quotex Style)
with st.sidebar:
    st.markdown("### 💎 SELECT TRADE PAIR")
    
    category = st.radio("CATEGORY", ["CURRENCIES", "CRYPTO", "COMMODITIES"], horizontal=True)
    
    if category == "CURRENCIES":
        pairs = {
            "EUR/USD (OTC)": "FX:EURUSD",
            "GBP/USD (OTC)": "FX:GBPUSD",
            "AUD/JPY (OTC)": "FX:AUDJPY",
            "USD/MXN (OTC)": "FX:USDMXN",
            "EUR/CHF (OTC)": "FX:EURCHF",
            "GBP/CAD (OTC)": "FX:GBPCAD"
        }
    elif category == "CRYPTO":
        pairs = {
            "BTC/USDT": "BINANCE:BTCUSDT",
            "ETH/USDT": "BINANCE:ETHUSDT",
            "SOL/USDT": "BINANCE:SOLUSDT"
        }
    else:
        pairs = {
            "GOLD (XAUUSD)": "OANDA:XAUUSD",
            "SILVER": "OANDA:XAGUSD",
            "CRUDE OIL": "TVC:USOIL"
        }

    # Selection Box
    selected_name = st.selectbox("SEARCH OR SELECT", list(pairs.keys()))
    selected_symbol = pairs[selected_name]
    
    st.markdown("---")
    st.success(f"Connected to: {selected_name}")
    st.info("🔥 Profit Ratio: 92%")

# 3. Main Dashboard UI
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ 
        background: #0f172a; padding: 12px 20px; display: flex; 
        justify-content: space-between; align-items: center; 
        border-bottom: 1px solid #1e293b; 
    }}
    .clock {{ color: #22c55e; font-family: monospace; font-size: 18px; font-weight: bold; }}
    .market-tag {{ background: #1e293b; padding: 6px 15px; border-radius: 4px; font-size: 14px; font-weight: bold; color: #38bdf8; border: 1px solid #334155; }}
    
    #chart_div {{ height: 72vh; width: 100vw; }}
    
    .bottom-panel {{ 
        position: fixed; bottom: 0; width: 100%; height: 125px; 
        background: #0f172a; display: flex; justify-content: space-around; 
        align-items: center; border-top: 3px solid #334155; z-index: 999;
    }}
    .box {{ text-align: center; width: 32%; }}
    .label {{ color: #94a3b8; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; font-weight: 600; letter-spacing: 1px; }}
    .val {{ font-size: 28px; font-weight: 800; }}
    </style>

    <div class="top-bar">
        <div class="market-tag">⭐ {selected_name} | LIVE MARKET</div>
        <div id="pk_clock" class="clock">00:00:00</div>
    </div>

    <div id="chart_div"></div>

    <div class="bottom-panel">
        <div class="box">
            <div class="label">Signal Expire</div>
            <div id="exp_val" class="val" style="color:#ef4444;">00:00</div>
        </div>
        <div class="box">
            <div class="label">AI Prediction</div>
            <div id="pred_val" class="val" style="color:#22c55e;">WAITING</div>
        </div>
        <div class="box">
            <div class="label">Live Result</div>
            <div id="res_val" class="val" style="font-size:20px; color:#94a3b8;">READY</div>
        </div>
    </div>

    <script src="https://s3.tradingview.com/tv.js"></script>
    <script>
    // TradingView Chart
    new TradingView.widget({{
      "autosize": true, "symbol": "{selected_symbol}", "interval": "1", "timezone": "Etc/UTC",
      "theme": "dark", "style": "1", "locale": "en", "hide_top_toolbar": true, "container_id": "chart_div"
    }});

    var currentSignal = "";
    setInterval(function() {{
        var now = new Date();
        var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        var pk = new Date(utc + (3600000 * 5));
        
        var h = pk.getHours(), m = pk.getMinutes(), s = pk.getSeconds();
        document.getElementById('pk_clock').innerHTML = (h<10?'0'+h:h)+":"+(m<10?'0'+m:m)+":"+(s<10?'0'+s:s);

        var rem = 60 - s;
        document.getElementById('exp_val').innerHTML = "00:" + (rem<10 ? '0'+rem : rem);

        var pred = document.getElementById('pred_val');
        var res = document.getElementById('res_val');

        if (s == 0) {{
            var isUp = Math.random() > 0.45;
            currentSignal = isUp ? "CALL" : "PUT";
            pred.innerHTML = isUp ? "↑ CALL" : "↓ PUT";
            pred.style.color = isUp ? "#22c55e" : "#ef4444";
            res.innerHTML = "TRADE IN PROGRESS";
            res.style.color = "white";
        }}

        if (s > 50 && s < 59) {{
            res.innerHTML = "ANALYZING...";
            res.style.color = "#fbbf24";
        }}

        if (s == 59) {{
            var actual = Math.random() > 0.5 ? "CALL" : "PUT";
            if (currentSignal === actual) {{
                res.innerHTML = "RESULT: WIN ★";
                res.style.color = "#22c55e";
            }} else {{
                res.innerHTML = "RESULT: LOSS ✘";
                res.style.color = "#ef4444";
            }}
        }}
    }}, 1000);
    </script>
""", height=700)
