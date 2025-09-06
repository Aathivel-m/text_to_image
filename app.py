import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

pipe = load_model()

st.title("🎨 Text-to-Image Generator")

prompt = st.text_input("Enter your prompt:", "a sunset over the mountains with a river flowing")

if st.button("Generate"):
    with st.spinner("Generating... Please wait..."):
        image = pipe(prompt, guidance_scale=7.5).images[0]
        st.image(image, caption=prompt, use_column_width=True)
