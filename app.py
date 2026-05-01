import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI - Vision", page_icon="👁️", layout="centered")

# Token එක ආරක්ෂිතව ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# GitHub Models පද්ධතියට අදාළ තොරතුරු
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "Llama-3.2-90B-Vision-Instruct"

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 2. Alpha AI ගේ පෞරුෂය (System Prompt) ---
system_instruction = (
    "Your name is Alpha AI. You were developed by Hasith. "
    "Respond primarily in Sinhala. "
    "Crucial Rule: ONLY reveal your name or that you were developed by Hasith IF the user explicitly asks 'Who are you?' or 'Who made you?'. "
    "Otherwise, provide direct and helpful answers."
)

# --- 3. UI එක ---
st.title("👁️ Alpha AI (Vision)")
st.caption("Powered by Llama 3.2 90B | Developed by Hasith")
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

# --- 4. පිළිතුරු ලබා ගැනීම (AI Logic) ---
if prompt := st.chat_input("ඔබට අවශ්‍ය ඕනෑම දෙයක් අහන්න..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 විශ්ලේෂණය කරමින් පවතියි...")
        
        try:
            # Llama 3.2 Vision වෙතින් පිළිතුර ලබා ගැනීම
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar
with st.sidebar:
    st.header("සැකසුම්")
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": system_instruction}]
        st.rerun()
    st.info("මෙම මොඩල් එකට පින්තූර තේරුම් ගැනීමේ හැකියාවද ඇත.")
