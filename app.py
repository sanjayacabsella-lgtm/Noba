import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI - GPT-4o", page_icon="🤖", layout="centered")

# Token එක ආරක්ෂිතව ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# GitHub Models හරහා GPT-4o සම්බන්ධ කිරීම
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o" # මෙය GitHub Marketplace හි ඇති සම්පූර්ණ GPT-4o මොඩල් එකයි

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 2. Alpha AI ගේ පෞරුෂය (System Prompt) ---
system_instruction = (
    "Your name is Alpha AI. You were developed by Hasith. "
    "Respond primarily in Sinhala. "
    "Strict Rule: ONLY reveal your identity as Alpha AI or that Hasith developed you IF the user explicitly asks 'Who are you?' or 'Who made you?'. "
    "Otherwise, provide direct, high-quality, and helpful answers without mentioning yourself or your creator."
)

# --- 3. UI එක ---
st.title("🤖 Alpha AI (GPT-4o)")
st.caption("Advanced Intelligence | Developed by Hasith")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# චැට් ඉතිහාසය පෙන්වීම
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 4. AI Logic ---
if prompt := st.chat_input("ඔබට අවශ්‍ය ඕනෑම දෙයක් අසන්න..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("📡 සම්බන්ධ වෙමින් පවතියි...")
        
        try:
            # GPT-4o වෙතින් පිළිතුර ලබා ගැනීම
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=4096
            )
            
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.header("සැකසුම්")
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "system", "content": system_instruction}]
        st.rerun()
    st.info("මෙය GPT-4o තාක්ෂණයෙන් ක්‍රියාත්මක වේ.")
