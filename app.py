import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Alpha AI - Image Lab",
    page_icon="🛡️",
    layout="centered"
)

# --- Fetch API Key from Secrets ---
# This ensures your key is hidden from the public
try:
    API_KEY = st.secrets["SILICON_API_KEY"]
except KeyError:
    st.error("API Key not found in Streamlit Secrets!")
    st.stop()

def generate_image(prompt):
    """Generates an image using SiliconFlow API (FLUX Model)"""
    url = "https://api.siliconflow.cn/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell", # High-quality Professional Model
        "prompt": prompt,
        "image_size": "1024x1024",
        "batch_size": 1,
        "num_inference_steps": 4 # Flux schnell works best with 4 steps
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['data'][0]['url']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

# --- UI Layout ---
st.title("🛡️ Alpha AI: Image Generation Lab")
st.markdown("Generate high-quality, professional images powered by **SiliconFlow API**.")

# User Input Section
with st.container():
    user_prompt = st.text_area(
        "Enter your creative prompt:",
        placeholder="e.g. A futuristic robot standing on a high mountain in Ella, Sri Lanka, cinematic lighting, 8k resolution",
        height=100
    )
    
    generate_btn = st.button("Generate Masterpiece 🚀", use_container_width=True)

# Processing Section
if generate_btn:
    if user_prompt.strip():
        with st.spinner("Alpha Engine is processing your request..."):
            result = generate_image(user_prompt)
            
            if result.startswith("http"):
                st.success("Image generated successfully!")
                st.image(result, caption="AI Generated Result", use_container_width=True)
                
                # Download Button
                st.download_button(
                    label="Download Image 📥",
                    data=requests.get(result).content,
                    file_name="alpha_generated_image.png",
                    mime="image/png"
                )
            else:
                st.error(f"Failed to generate image. {result}")
    else:
        st.warning("Please enter a prompt first!")

# --- Footer ---
st.divider()
st.caption("Alpha AI Core | Powered by Flux.1 & SiliconFlow")
