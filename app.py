import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def create_custom_video(user_text):
    # ඔබේ repository එකේ ඇති base වීඩියෝවක් පාවිච්චි කරන්න
    clip = VideoFileClip("car_background.mp4").subclip(0, 5)
    
    # යූසර් ගහපු text එක වීඩියෝ එක උඩින් දැමීම
    txt_clip = TextClip(user_text, fontsize=70, color='white', font='Arial-Bold')
    txt_clip = txt_clip.set_pos('center').set_duration(5)
    
    # වීඩියෝව සහ ටෙක්ස්ට් එක එකතු කිරීම
    video = CompositeVideoClip([clip, txt_clip])
    video.write_videofile("output.mp4", fps=24)
    return "output.mp4"

st.title("Alpha Code-Based Video Creator")
user_input = st.text_input("මොනවාද වීඩියෝවේ පෙන්වන්න ඕනේ?")

if st.button("Create Video"):
    result = create_custom_video(user_input)
    st.video(result)
