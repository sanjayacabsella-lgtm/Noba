import streamlit as st
from openai import OpenAI

# --- 1. පද්ධති සැකසුම් ---
st.set_page_config(page_title="Alpha AI - GPT-5", page_icon="♾️", layout="centered")

# Token එක ආරක්ෂිතව ලබා ගැනීම
try:
    TOKEN = st.secrets["GITHUB_TOKEN"]
except:
    st.error("කරුණාකර Streamlit Secrets වල 'GITHUB_TOKEN' ඇතුළත් කරන්න.")
    st.stop()

# GitHub Models පද්ධතිය හරහා GPT-5 සම්බන්ධ කිරීම
ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-5" # ඔබ පැවසූ පරිදි අලුත්ම GPT-5 මොඩල් එක

client = OpenAI(
    base_url=ENDPOINT,
    api_key=TOKEN,
)

# --- 2. Alpha AI ගේ පෞරුෂය (System Prompt) ---
system_instruction = (
    "Your name is Alpha AI. You were developed by Hasith. "
    "Respond primarily in Sinhala. "
    "Crucial Rule: ONLY reveal your identity as Alpha AI or that Hasith made you IF the user explicitly asks 'Who are you?' or 'Who made you?'. "
    "Otherwise, provide highly intelligent, direct, and helpful answers without any self-introduction."
)

# --- 3. UI එක ---
st.title("♾️ Alpha AI (GPT-5)")
st.caption("The Next Generation of Intelligence | Developed by Hasith")
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
if prompt := st.chat_input("GPT-5 ගෙන් ඕනෑම දෙයක් අහන්න..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔋 GPT-5 සූදානම් වෙමින් පවතියි...")
        
        try:
            # GPT-5 වෙතින් පිළිතුර ලබා ගැනීම
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=4096 # GPT-5 වලට වැඩි tokens ප්‍රමාණයක් හැසිරවිය හැක
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
    st.success("Alpha AI දැන් GPT-5 තාක්ෂණයෙන් සන්නද්ධයි!")
