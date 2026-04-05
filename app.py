import streamlit as st
import requests

# Streamlit පිටුවේ සැකසුම්
st.set_page_config(page_title="AI Image Generator", page_icon="🎨")

st.title("🎨 DeepAI Image Generator")
st.write("ඔබට අවශ්‍ය ඕනෑම දෙයක් ඉංග්‍රීසියෙන් පහතින් type කරන්න.")

# API Key එක මෙතන තියෙනවා
DEEPAI_API_KEY = "E8a49c96-caa4-4c64-ade9-444febf8e09c"

# User input ලබා ගැනීම
prompt = st.text_input("Enter your prompt:", "a futuristic robot in a jungle")

if st.button("Generate Image"):
    if prompt:
        with st.spinner("රූපය නිර්මාණය වෙමින් පවතී... කරුණාකර රැඳී සිටින්න."):
            # DeepAI API එකට request එක යැවීම
            response = requests.post(
                "https://api.deepai.org/api/text2img",
                data={'text': prompt},
                headers={'api-key': DEEPAI_API_KEY}
            )
            
            output = response.json()
            
            # ප්‍රතිඵලය පරීක්ෂා කිරීම
            if "output_url" in output:
                image_url = output["output_url"]
                st.image(image_url, caption=f"Generated: {prompt}", use_column_width=True)
                st.success("සාර්ථකයි!")
                
                # Download link එකක් ලබා දීම
                st.markdown(f"[Download Image]({image_url})")
            else:
                st.error("දෝෂයක් සිදු වුණා. ඔබේ API limit එක ඉවර වෙලා වෙන්න පුළුවන්.")
                st.write(output) # දෝෂය මොකක්ද කියලා බලාගන්න
    else:
        st.warning("කරුණාකර යමක් ඇතුළත් කරන්න.")

st.sidebar.info("Powerd by DeepAI API")
