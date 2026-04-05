import streamlit as st
import requests
import io

# පිටුවේ සැකසුම්
st.set_page_config(page_title="Cloudflare AI Generator", page_icon="☁️")

st.title("☁️ Cloudflare Free Image Generator")
st.write("Cloudflare Workers AI තාක්ෂණයෙන් නොමිලේ රූප සාදාගන්න.")

# ඔබේ විස්තර (ආරක්ෂිතව මෙතන තබා ඇත)
ACCOUNT_ID = "2974b71a6d3dab87c1216cfd085422c5"
API_TOKEN = "cfut_9fnpPTBN8loKK136ol2v4vJ8mMolXDM4HcvQ165vc7b9f2a1"

# Model එකේ URL එක
# මෙහිදී 'stable-diffusion-xl-lightning' කියන model එක පාවිච්චි කරමු
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# User input
prompt = st.text_input("ඔබට අවශ්‍ය රූපය ගැන ඉංග්‍රීසියෙන් ලියන්න:", "A futuristic car in a neon city, high resolution, 8k")

if st.button("Generate Image"):
    if prompt:
        with st.spinner("Cloudflare AI රූපය නිර්මාණය කරමින් පවතී..."):
            try:
                # Cloudflare එකට request එක යැවීම
                response = requests.post(
                    API_URL, 
                    headers=headers, 
                    json={"prompt": prompt}
                )
                
                if response.status_code == 200:
                    # රූපය සාර්ථකව ලැබුණොත්
                    image_bytes = response.content
                    st.image(image_bytes, caption=f"Result for: {prompt}", use_column_width=True)
                    
                    # Download button එකක් ලබා දීම
                    st.download_button(
                        label="Download Image",
                        data=image_bytes,
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                    st.success("සාර්ථකයි!")
                else:
                    st.error(f"දෝෂයක් සිදු වුණා: {response.status_code}")
                    st.write(response.json()) # දෝෂය කුමක්දැයි බැලීමට
                    
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    else:
        st.warning("කරුණාකර යමක් ලියන්න.")

st.sidebar.markdown("---")
st.sidebar.info("ඔබේ Cloudflare Free Tier එකේ දිනකට දෙන සීමාව ඇතුළත මෙය නොමිලේ පාවිච්චි කළ හැක.")
