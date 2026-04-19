import streamlit as st
from gradio_client import Client
import os

# ඇප් එකේ මාතෘකාව
st.title("AI Video Generator")

# පියවර 1: පරිශීලකයාගෙන් Prompt එක ලබා ගැනීම
prompt = st.text_input("ඔබට අවශ්‍ය වීඩියෝව ගැන විස්තර කරන්න:", placeholder="A futuristic robot in a neon city...")

if st.button("Generate Video"):
    if prompt:
        try:
            with st.spinner("වීඩියෝව නිර්මාණය වෙමින් පවතී... විනාඩි කිහිපයක් ගත විය හැක."):
                # පියවර 2: Gradio Client හරහා Free GPU Space එකකට සම්බන්ධ වීම
                # මෙහි Wan 2.1 හෝ වෙනත් ඕනෑම Space එකක නම ලබාදිය හැකියි
                client = Client("Wan-AI/Wan2.1-T2V-14B")
                
                # පියවර 3: වීඩියෝව Generate කිරීම
                result = client.predict(
                    prompt=prompt,
                    api_name="/predict"
                )
                
                # result වල එන්නේ වීඩියෝ ගොනුව තාවකාලිකව පවතින path එකයි
                video_path = result
                
                # පියවර 4: වීඩියෝව පෙන්වීම
                if os.path.exists(video_path):
                    st.success("වීඩියෝව සාර්ථකව නිර්මාණය කළා!")
                    st.video(video_path)
                else:
                    st.error("වීඩියෝ ගොනුව සොයා ගැනීමට නොහැකි විය.")
                    
        except Exception as e:
            st.error(f"දෝෂයක් සිදු විය: {e}")
    else:
        st.warning("කරුණාකර යම් විස්තරයක් (prompt) ඇතුළත් කරන්න.")
