import streamlit as st
import requests
import io
from PIL import Image
import random

# --- Page Setup ---
st.set_page_config(page_title="Alpha AI - Stable", page_icon="🛡️")
st.title("🛡️ Alpha AI: Pro Image Engine")

def generate_image_pro(prompt):
    # Prompt එක URL එකට ගැළපෙන සේ සැකසීම
    encoded_prompt = prompt.replace(" ", "%20")
    seed = random.randint(1, 999999)
    
    # මේක Cloudflare සහ Fast API හරහා රන් වෙන ඉතාමත් ස්ථාවර ලින්ක් එකක්
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
    
    try:
        response = requests.get(url, timeout=40)
        # ලැබෙන දත්ත පින්තූරයක්ද කියලා පරීක්ෂා කරනවා (Image headers check)
        if response.status_code == 200 and "image" in response.headers.get("Content-Type", "").lower():
            return response.content
        else:
            return None
    except:
        return None

# --- UI ---
user_input = st.text_area("මොන වගේ පින්තූරයක්ද ඕනේ?", placeholder="e.g. A realistic blue car on a Sri Lankan road...")

if st.button("Generate Now 🚀", use_container_width=True):
    if user_input.strip():
        with st.spinner("Alpha Engine is rendering your request..."):
            img_data = generate_image_pro(user_input)
            
            if img_data:
                try:
                    # මෙතැනදී තමයි කලින් Error එක ආවේ. දැන් අපි ඒක ආරක්ෂිතව කරනවා.
                    image = Image.open(io.BytesIO(img_data))
                    st.image(image, caption="Generated Successfully", use_container_width=True)
                    
                    st.download_button(
                        label="Download Image 📥",
                        data=img_data,
                        file_name="alpha_ai_image.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error("ලැබුණු දත්ත පින්තූරයක් නෙවෙයි. කරුණාකර නැවත උත්සාහ කරන්න.")
            else:
                st.error("සර්වර් එක කාර්යබහුලයි. තත්පර 5කින් නැවත Generate ඔබන්න.")
    else:
        st.warning("කරුණාකර විස්තරයක් ඇතුළත් කරන්න.")

st.divider()
st.caption("Alpha AI Stable v6.0 | HONOR X9c Optimized")
