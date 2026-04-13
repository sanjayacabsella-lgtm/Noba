import streamlit as st
import requests

# ඔබේ Cloudflare විස්තර මෙතැනට දාන්න
CLOUDFLARE_ACCOUNT_ID = "2974b71a6d3dab87c1216cfd085422c5"
CLOUDFLARE_API_TOKEN = "cfat_p4kEdb7MYrPDFbknGZQEw4aMIiIrMrrzLabJux6x622e899c"

def generate_image_cloudflare(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{2974b71a6d3dab87c1216cfd085422c5}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"
    headers = {"Authorization": f"Bearer {cfat_p4kEdb7MYrPDFbknGZQEw4aMIiIrMrrzLabJux6x622e899c}"}
    
    response = requests.post(url, headers=headers, json={"prompt": prompt})
    return response.content

st.title("🛡️ Alpha Pro Photo Lab")

user_input = st.text_input("රූපය ගැන ලියන්න:")

if st.button("Generate 🚀"):
    if user_input:
        with st.spinner("Alpha Engine වැඩ කරයි..."):
            try:
                img_bytes = generate_image_cloudflare(user_input)
                st.image(img_bytes, caption="Alpha Gen", use_container_width=True)
            except:
                st.error("සම්බන්ධතාවයේ ගැටලුවක්.")
