import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

API_URL = "https://922db765a6f1.ngrok-free.app/generate"  # replace with Colab's URL

st.title("🎨 Text-to-Image Generator")

prompt = st.text_input("Enter your prompt:", "a castle in the clouds at sunrise")

if st.button("Generate"):
    with st.spinner("Talking to Colab backend..."):
        response = requests.post(API_URL, json={"text": prompt})
        if response.status_code == 200:
            img_b64 = response.json()["image_base64"]
            img_bytes = base64.b64decode(img_b64)
            image = Image.open(BytesIO(img_bytes))
            st.image(image, caption=prompt, use_column_width=True)
        else:
            st.error("Backend error: " + response.text)

