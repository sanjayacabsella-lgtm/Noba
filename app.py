import streamlit as st
from openai import OpenAI

# --- පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI - DeepSeek R1", page_icon="🧠", layout="centered")

# Token එක ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# DeepSeek-R1 සඳහා GitHub Models Endpoint එක
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "DeepSeek-R1" # GitHub Models වල ඇති නම

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

st.title("🧠 Alpha AI (DeepSeek-R1)")
st.caption("The World's Leading Open Source Reasoning Model")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# චැට් ඉතිහාසය පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AI Logic
if prompt := st.chat_input("සංකීර්ණ ගැටලුවක් මෙතැන ලියන්න..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 DeepSeek-R1 කල්පනා කරමින් පවතියි...")
        
        try:
            # DeepSeek-R1 සමඟ සම්බන්ධ වීම
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=False # සරල බව සඳහා දැනට stream අක්‍රීය කර ඇත
            )
            
            full_response = response.choices[0].message.content
            
            # පිළිතුර පෙන්වීම
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"දෝෂයක් සිදු විය: {e}")

# Sidebar
with st.sidebar:
    st.info("DeepSeek-R1 යනු ඉතා ඉහළ තර්කන හැකියාවක් සහිත මොඩල් එකකි. මෙය ගණිතය සහ Coding සඳහා වඩාත් සුදුසුයි.")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
