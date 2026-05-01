import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI", page_icon="⚡", layout="centered")

# Token එක ආරක්ෂිතව ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# Gemini 1.5 Flash සඳහා GitHub Models Endpoint එක
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "Gemini-1.5-Flash" # GitHub Models වල ඇති නම

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 2. Alpha AI ගේ පෞරුෂය (System Prompt) ---
# මෙහිදී ඔබ ඉල්ලූ පරිදි නම සහ නිර්මාණකරු ගැන උපදෙස් ඇතුළත් කර ඇත.
system_instruction = (
    "ඔබේ නම Alpha AI. ඔබ ඉතා වේගවත් සහ බුද්ධිමත් සහායකයෙකි. "
    "කවුරුහරි ඔබේ නම හෝ ඔබව හැදුවේ කවුද කියා ඇහුවොත් පමණක් 'මගේ නම Alpha AI, මාව නිර්මාණය කළේ හසිත' යනුවෙන් පවසන්න. "
    "එසේ නොසොයන අවස්ථාවලදී කෙලින්ම ප්‍රශ්නයට පිළිතුරු දෙන්න. අනවශ්‍ය විස්තර එපා."
)

# --- 3. UI එක ---
st.title("⚡ Alpha AI (Turbo)")
st.caption("Powered by Gemini 1.5 Flash | Instant Responses")
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
if prompt := st.chat_input("ඔබට අවශ්‍ය ඕනෑම දෙයක් අහන්න..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Gemini 1.5 Flash සමඟ සම්බන්ධ වීම
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
            st.error(f"දෝෂයක් සිදු විය: {e}")

# Sidebar
with st.sidebar:
    st.success("දැන් Alpha AI ඉතා වේගවත්!")
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "system", "content": system_instruction}]
        st.rerun()
