import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් (Page Configuration) ---
st.set_page_config(page_title="Alpha AI", page_icon="🤖", layout="centered")

# --- 2. ආරක්ෂිතව Token එක ලබා ගැනීම (Security Step) ---
# Streamlit Cloud එකේ Secrets වල ඔබ ලබා දුන් නම මෙහි භාවිතා වේ
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o-mini"

# OpenAI Client එක සකස් කිරීම
client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 3. මෘදුකාංගයේ පෙනුම (UI Design) ---
st.title("🤖 Alpha AI v2.0")
st.caption("Developed by Hasith | Powered by GPT-4o mini")
st.divider()

# --- 4. මතකය පවත්වා ගැනීම (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "ඔබ බුද්ධිමත් සහායකයෙකි. ඔබේ නම Alpha AI වේ."}
    ]

# චැට් ඉතිහාසය පෙන්වීම
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. පිළිතුරු ලබා ගැනීම (AI Logic) ---
if prompt := st.chat_input("ඔබට උදව් කළ හැක්කේ කෙසේද?"):
    
    # පරිශීලකයාගේ පණිවිඩය සේව් කිරීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 සිතමින්...")
        
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.8,
            )
            
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"දෝෂයක් සිදු විය: {e}")

# Sidebar එක
with st.sidebar:
    if st.button("Clear Conversation"):
        st.session_state.messages = [{"role": "system", "content": "ඔබේ නම Alpha AI වේ."}]
        st.rerun()
