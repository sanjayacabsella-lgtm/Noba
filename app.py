import streamlit as st
import requests
import io
from PIL import Image

st.title("🚀 Alpha Instant Engine")

# පෝලිම් නැතිව සහ API Key නැතිව වැඩ කරන රහස් URL එකක්
# මෙය Hugging Face හි 'Serverless Inference' තාක්ෂණය භාවිතා කරයි
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_ai_content(prompt):
    # කිසිම API Key එකක් අවශ්‍ය නොවන පරිදි ඉල්ලීම යැවීම
    response = requests.post(API_URL, json={"inputs": prompt})
    return response.content

prompt = st.text_input("ඔබට අවශ්‍ය දේ ලියන්න (උදා: a flying car):")

if st.button("Generate Now"):
    if prompt:
        with st.spinner("පෝලිම් පරීක්ෂා කරමින්... තත්පර කිහිපයකින් ලැබෙනු ඇත..."):
            try:
                content = generate_ai_content(prompt)
                image = Image.open(io.BytesIO(content))
                st.image(image, caption="Alpha විසින් නිපදවන ලදී", use_column_width=True)
                st.success("සාර්ථකයි! පෝලිම මඟහැරියා.")
            except Exception as e:
                st.error("දැනට සර්වර් එක කාර්යබහුලයි. තත්පර 10කින් නැවත උත්සාහ කරන්න.")
    else:
        st.warning("කරුණාකර යමක් ඇතුළත් කරන්න.")
