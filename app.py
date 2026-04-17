import streamlit as st
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Alpha AI - Image Lab", page_icon="🎨", layout="centered")

st.title("🛡️ Alpha AI: Image Generation")
st.write("Generate high-quality images for free.")

def generate_image(user_prompt):
    # Prompt එකේ තියෙන හිස්තැන් URL එකට ගැළපෙන සේ සැකසීම
    encoded_prompt = user_prompt.replace(" ", "%20")
    timestamp = int(time.time())
    
    # පින්තූරය නිපදවන සෘජු API ලින්ක් එක
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={timestamp}&model=flux&nologo=true"
    
    return image_url

# --- UI Layout ---
user_input = st.text_area("What do you want to create?", 
                          placeholder="e.g. A beautiful view of Ella Rock Sri Lanka, cinematic 4k",
                          height=100)

if st.button("Generate Image 🚀", use_container_width=True):
    if user_input.strip():
        with st.spinner("Alpha Engine is creating your image..."):
            result_url = generate_image(user_input)
            
            # පින්තූරය පෙන්වීම
            st.image(result_url, caption=f"Result for: {user_input}", use_container_width=True)
            
            # Download Button එක (වැරැද්ද නිවැරදි කර ඇත)
            st.markdown(f'''
                <a href="{result_url}" target="_blank">
                    <button style="width:100%; border-radius:10px; background-color:#ff4b4b; color:white; padding:10px; border:none; cursor:pointer;">
                        Open Full Image & Download 📥
                    </button>
                </a>
            ''', unsafe_allow_html=True)
            
            st.success("Image generated successfully!")
    else:
        st.warning("Please enter a description first!")

st.divider()
st.caption("Alpha AI Core | High-Speed Image Generation")
