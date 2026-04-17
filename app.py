import streamlit as st
import requests
import io
from PIL import Image
import random

# --- Alpha Ultra-Masterpiece Setup ---
st.set_page_config(page_title="Alpha AI: Ultra-Masterpiece", page_icon="🔱", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .stButton>button { border: 2px solid #00ffcc; border-radius: 50px; background: linear-gradient(45deg, #00ffcc, #0077ff); color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 Alpha AI: Ultra-Masterpiece")
st.write("System Status: `Ready to Render` | Nodes: `10 Active Clusters`")

def alpha_smart_engine(prompt):
    seed = random.randint(1, 999999999)
    p = prompt.strip().replace(" ", "%20")
    
    # 🔱 සර්වර් පද්ධති 10ක් - මේවා එකිනෙකට වෙනස් රටවල පිහිටා ඇත
    nodes = [
        f"https://api.airforce/imagine2?prompt={p}&model=flux&width=1024&height=1024&seed={seed}",
        f"https://image.pollinations.ai/prompt/{p}?width=1024&height=1024&seed={seed}&model=flux&nologo=true",
        f"https://api.airforce/imagine2?prompt={p}&model=any-dark&width=1024&height=1024&seed={seed}",
        f"https://pollinations.ai/p/{p}?width=1024&height=1024&seed={seed}&model=flux-realism",
        f"https://image.pollinations.ai/prompt/{p}?width=1024&height=1024&seed={seed}&model=turbo",
        f"https://api.shuttleai.com/v1/bing/image?prompt={p}",
        f"https://api.airforce/imagine2?prompt={p}&model=flux-anime&seed={seed}",
        f"https://image.pollinations.ai/prompt/{p}?width=1024&height=1024&seed={seed}&model=sana",
        f"https://api.airforce/imagine2?prompt={p}&model=stable-diffusion-3.5&seed={seed}",
        f"https://pollinations.ai/p/{p}?width=1024&height=1024&seed={seed}&model=flux-pro"
    ]
    
    # ඉබේම මාරු වීමේ රහස (Auto-Shuffling)
    random.shuffle(nodes)

    for i, node in enumerate(nodes):
        try:
            # සර්වර් එක චෙක් කරනවා - තත්පර 12ක් ඇතුළත ප්‍රතිචාර නැත්නම් ඊළඟ එකට පනිනවා
            res = requests.get(node, timeout=12)
            if res.status_code == 200 and "image" in res.headers.get("Content-Type", "").lower():
                return res.content, node
        except:
            continue # මෙය තමයි ඉබේම මාරු වීමේ ක්‍රියාවලිය
    return None, None

# --- User Interface ---
user_input = st.text_input("ඔබේ සිතුවිල්ල (English):", placeholder="e.g. A high-tech laboratory in Ella, neon lighting, 8k cinematic")

if st.button("RENDER INFINITY ART 🚀"):
    if user_input:
        status = st.empty()
        status.warning("🔄 Connecting to the fastest node in the cluster...")
        
        img_data, node_url = alpha_smart_engine(user_input)
        
        if img_data:
            status.empty()
            image = Image.open(io.BytesIO(img_data))
            st.image(image, caption="Rendered by Alpha Ultra-Masterpiece Engine", use_container_width=True)
            
            st.download_button(
                label="Download 4K Quality 📥",
                data=img_data,
                file_name=f"alpha_master_{random.randint(100,999)}.jpg",
                mime="image/jpeg",
            )
            st.success(f"Success! Handled by Server: {node_url.split('/')[2]}")
        else:
            status.error("සියලුම සර්වර්ස් අතිශය කාර්යබහුලයි. තත්පර 5කින් නැවත උත්සාහ කරන්න.")
    else:
        st.warning("කරුණාකර විස්තරයක් ලියන්න.")

st.divider()
st.caption("Alpha AI v12.0 Ultra-Masterpiece | Distributed Autonomous Network | No Manual Switching Needed")
