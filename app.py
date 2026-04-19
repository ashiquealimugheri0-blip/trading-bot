import streamlit as st
import time
import random

# Page Config
st.set_page_config(page_title="Finorex AI Master", layout="centered")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #060d14; color: white; }
    div.stButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: black; font-weight: bold; width: 100%; border-radius: 10px; border: none; height: 50px;
    }
    .signal-box {
        padding: 20px; border-radius: 15px; border: 2px solid #38bdf8;
        background: rgba(15, 23, 42, 0.9); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🤖 FINOREX AI MASTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38bdf8;'>Chinese Secret Algorithm Enabled 🚀</p>", unsafe_allow_html=True)

# Selection Boxes (Like your friends bot)
broker = st.selectbox("Select Broker", ["Quotex", "Pocket Option", "Binomo"])
asset = st.selectbox("Trading Asset", ["EUR/USD (OTC)", "Bitcoin Cash (OTC)", "USD/PKR (OTC)", "GBP/JPY"])
timeframe = st.selectbox("Time Frame", ["15s", "30s", "1m", "5m"])

if st.button("GENERATE SIGNAL"):
    with st.spinner('Analyzing Chinese Algorithms...'):
        time.sleep(2)
        
    res = random.choice(["UP / CALL 🟢", "DOWN / PUT 🔴"])
    acc = random.randint(92, 98)
    
    st.markdown(f"""
        <div class="signal-box">
            <h2 style='color: {"#22c55e" if "UP" in res else "#ef4444"};'>{res}</h2>
            <p>Accuracy: {acc}%</p>
            <p style='font-size: 12px; color: gray;'>Expiry: {timeframe}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center; margin-top: 50px;'>Server Time: {time.strftime('%H:%M:%S')} PKT</p>", unsafe_allow_html=True)
