import streamlit as st
import os
from groq import Groq
from moviepy.editor import VideoFileClip
import json

# Mobile-friendly Page Configuration
st.set_page_config(page_title="AI Smart Video Clipper", page_icon="🎬", layout="centered")

st.title("🎬 AI Smart Video Clipper")
st.write("වීඩියෝවක් ලබා දී, ඔබට අවශ්‍ය කොටස Prompt එකකින් පවසන්න. (High-Speed Optimized)")

# Sidebar for Groq API Key
groq_api_key = st.sidebar.text_input("Groq API Key එක ඇතුළත් කරන්න:", type="password")

if groq_api_key:
    # Initialize Groq Client
    client = Groq(api_key=groq_api_key)

    # 1. Video Upload Component
    uploaded_file = st.file_input("ඔබේ වීඩියෝව මෙතැනට Upload කරන්න (MP4):", type=["mp4"])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.video("temp_video.mp4")
        st.success("වීඩියෝව සාර්ථකව Upload විය!")

        # 2. User Prompt Input
        user_prompt = st.text_input("ඔබට කට් කර ගැනීමට අවශ්‍ය කුමන කොටසද? (उदा: 'ඇල්බට් අයින්ස්ටයින් ගැන කියන කොටස')", "")

        if st.button("AI Cut වීඩියෝව සාදන්න 🚀"):
            if user_prompt:
                # --- STEP 1: AUDIO EXTRACTION ---
                with st.spinner("පළමුව වීඩියෝවේ Audio එක වෙන් කරමින් පවතී..."):
                    try:
                        video_clip = VideoFileClip("temp_video.mp4")
                        video_clip.audio.write_audiofile("temp_audio.mp3", logger=None)
                        video_clip.close()
                    except Exception as e:
                        st.error(f"Audio Extraction Error: {e}")
                        st.stop()

                # --- STEP 2: WHISPER SPEECH-TO-TEXT ---
                with st.spinner("AI මඟින් වීඩියෝවේ කතාව කියවමින් පවතී (Transcribing)..."):
                    try:
                        with open("temp_audio.mp3", "rb") as audio_file:
                            transcript_response = client.audio.transcriptions.create(
                                file=("temp_audio.mp3", audio_file.read()),
                                model="whisper-large-v3",
                                response_format="verbose_json"
                            )
                        
                        segments = transcript_response.segments
                        formatted_transcript = "".join([f"[{s['start']}s - {s['end']}s]: {s['text']}\n" for s in segments])
                        os.remove("temp_audio.mp3") # Clean up audio file
                    except Exception as e:
                        st.error(f"Whisper Transcription Error: {e}")
                        st.stop()

                # --- STEP 3: LLM TIMESTAMP DETECTION ---
                with st.spinner("ඔබේ Prompt එක අනුව අවශ්‍ය කොටස AI එක මඟින් සොයමින් පවතී..."):
                    try:
                        llm_prompt = f"""
                        You are an expert video editor. I will give you a transcript of a video with timestamps and a user request.
                        Your job is to find the exact 'start_time' and 'end_time' from the transcript that best matches the user's request.

                        Transcript:
                        {formatted_transcript}

                        User Request: {user_prompt}

                        Provide your response ONLY as a raw JSON object with 'start' and 'end' keys (values in seconds as float). Do not include any thinking or extra text.
                        Example format: {{"start": 12.5, "end": 45.2}}
                        """

                        chat_completion = client.chat.completions.create(
                            messages=[{"role": "user", "content": llm_prompt}],
                            model="llama3-8b-8192",
                            temperature=0.0
                        )

                        response_text = chat_completion.choices[0].message.content.strip()
                        time_data = json.loads(response_text)
                        
                        start_sec = float(time_data['start'])
                        end_sec = float(time_data['end'])
                        
                        st.info(f"🎯 AI තීරණය: තත්පර {start_sec} සිට තත්පර {end_sec} දක්වා කොටස.")
                    except Exception as e:
                        st.error(f"AI Timestamp Detection Error: {e}")
                        st.stop()

                # --- STEP 4: HIGH-SPEED VIDEO RENDERING ---
                with st.spinner("MoviePy මඟින් වීඩියෝව High-Speed Render වෙමින් පවතී..."):
                    try:
                        main_clip = VideoFileClip("temp_video.mp4")
                        trimmed_clip = main_clip.subclip(start_sec, end_sec)
                        
                        # Optimization Settings: 
                        # preset='ultrafast' (Rendering වේගය 5 ගුණයකින් වැඩි කරයි)
                        # threads=4 (Server එකේ CPU Cores 4ක් එකවර පාවිච්චි කරයි)
                        trimmed_clip.write_videofile(
                            "output_short.mp4", 
                            codec="libx264", 
                            audio_codec="aac", 
                            preset="ultrafast", 
                            threads=4, 
                            logger=None
                        )
                        main_clip.close()
                        trimmed_clip.close()
                        
                        st.success("ඔබේ වීඩියෝව සාර්ථකව සූදානම් කර ඇත! 🎉")
                        st.video("output_short.mp4")

                        # Mobile-friendly Download Button
                        with open("output_short.mp4", "rb") as file:
                            st.download_button(
                                label="වීඩියෝව Phone එකට Download කරගන්න 📥",
                                data=file,
                                file_name="ai_short.mp4",
                                mime="video/mp4"
                            )
                        
                        # Clean up output file after rendering
                        os.remove("output_short.mp4")
                        
                    except Exception as e:
                        st.error(f"Video Rendering Error: {e}")
            else:
                st.warning("කරුණාකර ඔබට අවශ්‍ය කොටස පිළිබඳ Prompt එකක් ඇතුළත් කරන්න.")
else:
    st.info("වැඩේ පටන් ගන්න Groq API Key එක Sidebar එකට ලබාදෙන්න.")
