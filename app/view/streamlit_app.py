"""
ASL Alphabet — Streamlit Frontend  
Run:  streamlit run streamlit_app.py
"""
import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:8000/api"

# ─── Page Config ───
st.set_page_config(page_title="ASL Classifier", page_icon="", layout="wide")

# ─── Custom CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Poppins', sans-serif;
    }

    /* Header bar */
    .header-bar {
        background: linear-gradient(90deg, #1a1a2e, #2d2d44, #1a1a2e);
        border-bottom: 3px solid #f39c12;
        padding: 18px;
        text-align: center;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
    }
    .header-bar h1 {
        color: #ffffff;
        font-size: 2.4rem;
        margin: 0;
        font-weight: 700;
    }
    .header-bar h1 span {
        color: #f39c12;
    }

    /* Description card */
    .desc-card {
        background: rgba(30, 30, 50, 0.85);
        border: 1px solid #333;
        border-radius: 16px;
        padding: 30px;
        margin-top: 40px;
        backdrop-filter: blur(10px);
    }
    .desc-card h2 {
        color: #ffffff;
        font-size: 1.8rem;
        margin-bottom: 10px;
    }
    .desc-card h2 span {
        color: #f39c12;
        font-weight: 700;
    }
    .desc-card p {
        color: #cccccc;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    .desc-card .emoji-row {
        font-size: 2.5rem;
        margin-top: 20px;
        letter-spacing: 12px;
    }

    /* Upload card */
    .upload-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin-top: 40px;
    }

    /* Result card */
    .result-card {
        background: rgba(30, 30, 50, 0.9);
        border: 1px solid #27ae60;
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
    }
    .result-card h3 {
        color: #27ae60;
        font-size: 1.6rem;
        text-align: center;
    }
    .pred-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #333;
        color: #eee;
        font-size: 1.05rem;
    }
    .pred-row:last-child { border-bottom: none; }
    .pred-label { font-weight: 600; }
    .pred-conf { color: #f39c12; font-weight: 700; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #27ae60, #2980b9) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 40px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 15px;
    }

    /* Hide streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Header ───
st.markdown("""
<div class="header-bar">
    <h1> ASL Alphabet <span>Classification</span> </h1>
</div>
""", unsafe_allow_html=True)

# ─── Layout: Left description + Right upload ───
col_left, col_space, col_right = st.columns([5, 1, 4])

with col_left:
    st.markdown("""
    <div class="desc-card">
        <h2>🧠 ASL Alphabet <span>Classification</span></h2>
        <p>
            🖐️ American Sign Language (ASL) alphabet recognition powered by a
            <b>fine-tuned ResNet50</b> deep learning model. Upload a hand sign
            image and get instant predictions across <b>29 classes</b>
            (A–Z + delete, nothing, space).
        </p>
        <p>
            📸 Simply upload your image on the right and hit <b>Predict</b> to see
            the top-5 classifications with confidence scores!
        </p>
        <div class="emoji-row">🅰️ 🅱️ 🤙 👆 ✌️ 🤟</div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="upload-card">', unsafe_allow_html=True)
    uploaded = st.file_uploader("📤 Choose a hand sign image", type=["jpg", "jpeg", "png"])

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="📷 Uploaded Image", use_container_width=True)

        if st.button("🔮 Predict"):
            try:
                with st.spinner("🔄 Classifying..."):
                    uploaded.seek(0)
                    files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
                    res = requests.post(f"{API_URL}/predict", files=files)

                if res.status_code == 200:
                    data = res.json()
                    st.markdown(f"""
                    <div class="result-card">
                        <h3>✅ Prediction: {data['top_label']}  ({data['top_confidence']}%)</h3>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {res.json().get('detail', res.text)}")

            except requests.exceptions.ConnectionError:
                st.error("⚠️ Cannot connect to FastAPI. Start the server first:\n\n"
                         "`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`")
    else:
        st.markdown("""
        <div style="border: 2px dashed #ccc; border-radius: 12px; padding: 60px 20px;
                    text-align: center; color: #999; margin: 10px 0;">
            <span style="font-size: 3rem;">🖼️</span><br>
            <span>No image selected</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
