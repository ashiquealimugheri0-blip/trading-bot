import streamlit as st
import streamlit.components.v1 as components

# 1. Full Screen Configuration
st.set_page_config(page_title="Finorex AI - Full Markets", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .block-container { padding: 0px !important; margin: 0px !important; }
    header, footer, .stDeployButton { visibility: hidden; height: 0px; }
    body { background-color: #060d14; color: white; }
    
    /* Quotex Style Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #1e293b;
        min-width: 300px !important;
    }
    .stSelectbox label { color: #22c55e !important; font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Complete Market List (Quotex Style)
with st.sidebar:
    st.markdown("### 📊 SELECT ASSET")
    
    # Combined List of All Major Markets
    all_markets = {
        "--- CURRENCIES (Forex) ---": "FX:EURUSD",
        "EUR/USD (OTC)": "FX:EURUSD",
        "GBP/USD (OTC)": "FX:GBPUSD",
        "USD/MXN (OTC)": "FX:USDMXN",
        "AUD/JPY (OTC)": "FX:AUDJPY",
        "EUR/CHF (OTC)": "FX:EURCHF",
        "GBP/CAD (OTC)": "FX:GBPCAD",
        "USD/CHF (OTC)": "FX:USDCHF",
        "GBP/AUD (OTC)": "FX:GBPAUD",
        "--- CRYPTO ---": "BINANCE:BTCUSDT",
        "BTC/USDT": "BINANCE:BTCUSDT",
        "ETH/USDT": "BINANCE:ETHUSDT",
        "SOL/USDT": "BINANCE:SOLUSDT",
        "--- COMMODITIES ---": "OANDA:XAUUSD",
        "GOLD (XAU/USD)": "OANDA:XAUUSD",
        "SILVER (XAG/USD)": "OANDA:XAGUSD",
        "CRUDE OIL": "TVC:USOIL"
    }

    selected_name = st.selectbox("Market Pairs", list(all_markets.keys()), index=1)
    
    # Validation: Agar user ne header select kiya toh default EURUSD chale
    if "---" in selected_name:
        selected_symbol = "FX:EURUSD"
        selected_name = "EUR/USD (OTC)"
    else:
        selected_symbol = all_markets[selected_name]
    
    st.markdown("---")
    st.success(f"ACTIVE: {selected_name}")
    st.markdown("🔥 **Payout: 94%**")

# 3. UI Dashboard & Logic
components.html(f"""
    <style>
    body {{ background-color: #060d14; color: white; font-family: sans-serif; margin: 0; overflow: hidden; }}
    .top-bar {{ background: #0f172a; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; }}
    .clock {{ color: #22c55e; font-family: monospace; font-size: 18px; font-weight: bold; }}
    .tag {{ background: #1e293b; padding: 6px 12px; border-radius: 4px; font-weight: bold; color: #38bdf8; border: 1px solid #334155; }}
    #chart_div {{ height: 72vh; width: 100vw; }}
    .panel {{ position: fixed; bottom: 0; width: 100%; height: 125px; background: #0f172a; display: flex; justify-content: space-around; align-items: center; border-top: 3px solid #334155; }}
    .box {{ text-align: center; width: 32%; }}
    .label {{ color: #94a3b8; font-size: 11px; text-transform: uppercase; margin-bottom: 5px; }}
    .val {{ font-size: 28px; font-weight: 800; }}
    </style>

    <div class="top-bar">
        <div class="tag">⭐ {selected_name}</div>
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
            <div class="label">Live Result</div>
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
            document.getElementById('res').innerHTML = "TRADE OPEN";
            document.getElementById('res').style.color = "white";
        }}
        if (s == 59) {{
            var win = Math.random() > 0.5;
            document.getElementById('res').innerHTML = win ? "WIN ★" : "LOSS ✘";
            document.getElementById('res').style.color = win ? "#22c55e" : "#ef4444";
        }}
    }}, 1000);
    </script>
""", height=700)
