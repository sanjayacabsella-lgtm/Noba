import streamlit as st
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Alpha AI - Image Lab", page_icon="🎨", layout="centered")

st.title("🛡️ Alpha AI: Image Generation")
st.write("Generate high-quality images for free. No API Key required.")

def generate_image(user_prompt):
    # අපි පාවිච්චි කරන්නේ පෝලිම් නැති, Prompt එක අනුව වෙනස් වන Public API එකක්
    # මෙහිදී 'seed' එක වෙනස් කිරීමෙන් හැමවිටම අලුත් පින්තූරයක් ලැබේ
    timestamp = int(time.time())
    
    # Prompt එකේ තියෙන හිස්තැන් (Spaces) URL එකට ගැළපෙන සේ සැකසීම
    encoded_prompt = user_prompt.replace(" ", "%20")
    
    # මේක ලෝකයේ තියෙන හොඳම Free Image Engine එකක් (Unsplash/Source ආශ්‍රිතව නෙවෙයි, සැබෑ AI එකක්)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={timestamp}&model=flux-realism&nologo=true"
    
    return image_url

# --- UI Layout ---
with st.container():
    user_input = st.text_area("What do you want to create?", 
                              placeholder="e.g. A luxury van driving in Ella Sri Lanka, 4k, realistic",
                              height=100)
    
    generate_btn = st.button("Generate Image 🚀", use_container_width=True)

if generate_btn:
    if user_input.strip():
        with st.spinner("Alpha Engine is creating your image..."):
            result_url = generate_image(user_input)
            
            # පින්තූරය පෙන්වීම
            st.image(result_url, caption=f"Result for: {user_input}", use_container_width=True)
            
            # Download Button එකක් ලබා දීම
            st.markdown(f'''
                <a href="{result_url}" download="alpha_ai_image.png">
                    <button style="width:100%; border-radius:10px; background-color:#ff4b4b; color:white; padding:10px; border:none; cursor:pointer;">
                        Download Full Image 📥
                    </button>
                </a>
            ''', unsafe_allow_ Harris=True)
            
            st.success("Image generated successfully!")
    else:
        st.warning("Please enter a description first.")

st.divider()
st.caption("Alpha AI Core | High-Speed Image Generation")
