import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI", page_icon="🤖", layout="centered")

# Token එක ආරක්ෂිතව ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# GitHub Models Endpoint
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 2. Alpha AI ගේ පෞරුෂය ---
system_instruction = (
    "Your name is Alpha AI. You were developed by Hasith. "
    "Respond primarily in Sinhala. "
    "ONLY reveal your identity or creator if specifically asked. "
    "Provide helpful and intelligent responses."
)

# --- 3. UI නිර්මාණය ---
st.title("🤖 Alpha AI")
st.caption("Developed by Hasith | GPT-4o Streaming Enabled")
st.divider()

# පණිවිඩ මතකය පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# පණිවිඩ ඉතිහාසය පෙන්වීම
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 4. Streaming Logic ---
if prompt := st.chat_input("ඔබට අවශ්‍ය ඕනෑම දෙයක් අසන්න..."):
    
    # පරිශීලක පණිවිඩය සේව් කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර Streaming හරහා ලබා ගැනීම
    with st.chat_message("assistant"):
        # "Thinking" යනුවෙන් පෙන්වන කොටස
        status_placeholder = st.empty()
        status_placeholder.markdown("🔍 *Alpha AI කල්පනා කරමින් පවතියි...*")
        
        try:
            # stream=True ලබා දීමෙන් අකුරෙන් අකුර ලබා ගත හැක
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7,
                stream=True
            )
            
            # පණිවිඩය තිරය මත අකුරෙන් අකුර පෙන්වීම
            status_placeholder.empty() # "Thinking" පණිවිඩය ඉවත් කරයි
            full_response = st.write_stream(stream)
            
            # සම්පූර්ණ පිළිතුර මතකයට එකතු කිරීම
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "system", "content": system_instruction}]
        st.rerun()
