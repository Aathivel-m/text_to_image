import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Replace this with your Colab backend URL

API_URL = "https://17cc-34-169-105-210.ngrok-free.app/generate"


st.set_page_config(
    page_title="Text to Image Generator",
    page_icon="🎨",
    layout="centered",               # switched to centered for a cleaner UI
    initial_sidebar_state="collapsed"
)


st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("⚙️ Settings")
    guidance_scale = st.slider("Guidance Scale", 1.0, 15.0, 7.5, 0.5)
    image_size = st.radio("Image Size", ["512x512", "768x768"])
    dark_mode = st.toggle("🌗 Dark Theme Preview", value=False)


st.markdown(
    """
    # 🎨 Text-to-Image Generator
    Generate **AI-powered images** from your imagination using Stable Diffusion.  
    Type a prompt below and watch your words turn into art!
    """,
    unsafe_allow_html=True,
)


prompt = st.text_area(
    "📝 Enter your creative prompt:",
    "a futuristic city skyline at night with flying cars",
    height=100,
)


if st.button("🚀 Generate Image"):
    with st.spinner("🎨 Creating your masterpiece... please wait..."):
        try:
            # Send request to backend
            payload = {"text": f"{prompt}, {image_size}, scale={guidance_scale}"}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                # Decode Base64 image
                img_b64 = response.json()["image_base64"]
                img_bytes = base64.b64decode(img_b64)
                image = Image.open(BytesIO(img_bytes))

                # Optional dark mode preview
                if dark_mode:
                    st.image(image, caption="🌙 Dark Mode Preview", use_container_width=True)
                    st.markdown("<p style='text-align:center;'>Dark theme version</p>", unsafe_allow_html=True)
                else:
                    st.image(image, caption=prompt, use_container_width=True)

            else:
                st.error("Backend error: " + response.text)
        except Exception as e:
            st.error(f"⚠️ Connection failed: {e}")


with st.expander("🔧 Advanced Settings"):
    st.slider("Learning Rate (Demo)", 0.0001, 0.01, 0.001)


st.markdown(
    """
    ---
    👩‍💻 Built with [Streamlit](https://streamlit.io/)  
    🚀 Powered by Stable Diffusion on Google Colab  
    """,
    unsafe_allow_html=True,
)

