import streamlit as st
import requests
import io
import json

# පිටුවේ සැකසුම් (Page Settings)
st.set_page_config(page_title="AI Art Studio", page_icon="🎨", layout="centered")

st.title("🎨 AI Multi-Style Art Studio")
st.write("ඔබට අවශ්‍ය රූපය ගැන ඉංග්‍රීසියෙන් ලියා, පහතින් කැමති කලා ශෛලිය (Style) තෝරන්න.")

# --- ආරක්‍ෂිත තොරතුරු (ඔබේ Cloudflare විස්තර) ---
# **වැදගත්:** GitHub එකට දානකොට මේවා Secrets වල දාන්න.
ACCOUNT_ID = "2974b71a6d3dab87c1216cfd085422c5"
API_TOKEN = "cfut_9fnpPTBN8loKK136ol2v4vJ8mMolXDM4HcvQ165vc7b9f2a1"

# --- Art Styles සහ Prompts ---
styles = {
    "Cartoon Style (Pixar)": {
        "model": "@cf/lykon/dreamshaper-8-lcm",
        "prompt_prefix": "3d render, Pixar style, Disney animation, cute character, high quality, vibrant colors, "
    },
    "Comic Book Style": {
        "model": "@cf/lykon/dreamshaper-8-lcm",
        "prompt_prefix": "comic book style, bold lines, colorful, graphic novel illustration, dramatic lighting, "
    },
    "Anime Style (Japanese)": {
        "model": "@cf/lykon/dreamshaper-8-lcm",
        "prompt_prefix": "anime style, vibrant colors, 2d illustration, studio ghibli style, detailed background, "
    },
    "Ultra Realistic": {
        "model": "@cf/bytedance/stable-diffusion-xl-lightning",
        "prompt_prefix": "ultra realistic, photorealistic, 8k, highly detailed, professional photography, cinematic, "
    }
}

# --- User Inputs ---
# 1. Prompt
user_prompt = st.text_input("Enter your request:", "A brave lion")

# 2. Select Style (Select Box)
selected_style_name = st.selectbox("Select Art Style:", list(styles.keys()))

# --- Generation Logic ---
if st.button("Generate Art"):
    if user_prompt:
        # තෝරාගත් Style එකේ විස්තර ලබා ගැනීම
        style_info = styles[selected_style_name]
        
        # අවසාන Prompt එක සැකසීම (Style Prefix + User Prompt)
        final_prompt = style_info["prompt_prefix"] + user_prompt
        
        # Model URL එක සැකසීම
        API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{style_info['model']}"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        
        with st.spinner(f"{selected_style_name} මගින් රූපය නිර්මාණය කරමින් පවතී..."):
            try:
                # Cloudflare API එකට Request එක යැවීම
                # JSON data: prompt සහ negative prompt (optional)
                json_data = {
                    "prompt": final_prompt,
                    "negative_prompt": "low quality, blurry, distorted, unrealistic eyes, bad anatomy"
                }
                
                response = requests.post(API_URL, headers=headers, json=json_data)
                
                if response.status_code == 200:
                    # රූපය සාර්ථකව ලැබුණොත්
                    image_bytes = response.content
                    st.image(image_bytes, caption=f"{selected_style_name}: {user_prompt}", use_column_width=True)
                    
                    # Download button
                    st.download_button(
                        label="Download Art",
                        data=image_bytes,
                        file_name=f"{user_prompt.replace(' ', '_')}_{selected_style_name}.png",
                        mime="image/png"
                    )
                    st.success("සාර්ථකයි!")
                else:
                    st.error(f"දෝෂයක් සිදු වුණා: {response.status_code}")
                    st.write(response.json())
                    
            except Exception as e:
                st.error(f"Unexpected error: {e}")
    else:
        st.warning("කරුණාකර යමක් ලියන්න.")

st.sidebar.markdown("---")
st.sidebar.info("ඔබේ Cloudflare Free Tier එකේ දිනකට දෙන සීමාව ඇතුළත මෙය නොමිලේ පාවිච්චි කළ හැක.")
