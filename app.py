import streamlit as st
from gradio_client import Client
import os

st.set_page_config(page_title="Alpha Video Engine", layout="wide")
st.title("🚀 Alpha Instant Video (No API Key)")

prompt = st.text_input("ඔබේ වීඩියෝ විස්තරය මෙහි ලියන්න:", placeholder="A cinematic shot of a robot in a rain forest...")

if st.button("Generate Video Now"):
    if prompt:
        try:
            with st.spinner("AI මාදිලියට සම්බන්ධ වෙමින් පවතී... පෝලිම් පරීක්ෂා කරයි..."):
                # මෙතනදී අපි පාවිච්චි කරන්නේ Public Space එකක්. 
                # මෙය API Key එකක් ඉල්ලන්නේ නැත.
                # සටහන: මෙම URL එක කාලෙන් කාලෙට වෙනස් විය හැක.
                client = Client("fffiloni/stable-video-diffusion") 

                st.info("පෝලිමේ සිටී නම් කරුණාකර රැඳී සිටින්න. මෙය 100% නොමිලේ ක්‍රමයකි.")
                
                result = client.predict(
                    input_video=None, # Text to Video සඳහා මෙය හිස්ව තබන්න
                    prompt=prompt,
                    api_name="/video_gen" # Space එකේ ඇති API endpoint එක
                )
                
                # වීඩියෝව පෙන්වීම
                if result:
                    st.success("වීඩියෝව සූදානම්!")
                    st.video(result)
                else:
                    st.error("වීඩියෝව සෑදීමට නොහැකි විය. පසුව උත්සාහ කරන්න.")
                    
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("සමහර විට මෙම Space එක අධික කාර්යබහුල විය හැක. වෙනත් Public Space එකක් පාවිච්චි කර බලමු.")
    else:
        st.warning("කරුණාකර Prompt එකක් ඇතුළත් කරන්න.")
