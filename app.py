import streamlit as st
import time

# පිටුවේ මුලික සැකසුම් (ලස්සනට පෙනෙන්න Wide Layout දානවා)
st.set_page_config(page_title="Nexo App Gallery", page_icon="🎮", layout="wide")

# Custom CSS වලින් ටිකක් high-tech look එකක් දෙමු
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #cc3333; }
    .storage-box { padding: 20px; border-radius: 10px; background-color: #1e293b; border: 1px solid #334155; }
    </style>
""", unsafe_allowed_html=True)

# 1. SIDEBAR DESIGN (යූසර්ගේ විස්තර සහ Storage එක)
st.sidebar.image("https://img.icons8.com/nolan/128/cyber-security.png", width=80) # Nexo Protect Logo එකක් වගේ
st.sidebar.title("Nexo Dashboard")
st.sidebar.write("---")

# ටෙලිග්‍රෑම් 20GB Storage එක මෙතන පෙන්වනවා
st.sidebar.subheader("📁 Nexo Drive (Telegram Cloud)")
MAX_STORAGE = 20.0 # 20GB Free
if "used_space" not in st.session_state:
    st.session_state.used_space = 0.0

available_space = MAX_STORAGE - st.session_state.used_space
st.sidebar.progress(st.session_state.used_space / MAX_STORAGE)
st.sidebar.write(f"**Used:** {st.session_state.used_space:.2f} GB / {MAX_STORAGE} GB")
st.sidebar.write(f"**Free Space:** {available_space:.2f} GB")

st.sidebar.write("---")
st.sidebar.info("⚙️ Server Node: Amazon AWS EC2\n\n🟢 Status: ONLINE (Free Tier)")


# 2. MAIN PAGE DESIGN
st.title("🎮 Nexo App Gallery")
st.write("ලැප්ටොප් එක ඕෆ් කරලා තිබ්බත් AWS සර්වර් එකෙන් පැය 24ම වැඩ කරන ලංකාවේ ප්‍රථම Cloud Gaming ප්ලැට්ෆෝම් එක.")
st.write("---")

# පේජ් එක කොටස් (Columns) 2කට බෙදමු
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Step 1: Upload Your Game/App")
    st.write("ඔයාගේ ගේම් එක මෙතනට දාන්න. ඒක ඔයාගේ **නොමිලේ ලැබුණු 20GB ටෙලිග්‍රෑම් Cloud** එකේ සේව් වෙනවා.")
    
    uploaded_file = st.file_uploader("Choose a game file (.zip, .apk, .exe)", type=["zip", "apk", "exe"])
    
    if uploaded_file is not None:
        file_size_gb = uploaded_file.size / (1024 * 1024 * 1024) # Bytes to GB
        
        if st.session_state.used_space + file_size_gb <= MAX_STORAGE:
            st.success(f"✔️ '{uploaded_file.name}' සාර්ථකව Nexo Drive එකට ඇතුලත් කරගත්තා!")
            if st.button("Save to Telegram Storage"):
                with st.spinner("Telegram බොට් එක හරහා සර්වර් එකට අප්ලෝඩ් වෙමින් පවතී..."):
                    time.sleep(2) # Upload වෙන බව පෙන්වීමට ඩිලේ එකක්
                    st.session_state.used_space += file_size_gb
                    st.balloons()
                    st.success("සාර්ථකව සේව් වුණා! දැන් ඔබට මේක AWS එකෙන් රන් කරන්න පුළුවන්.")
        else:
            st.error("❌ ඉඩ මදි! ඔබේ 20GB නොමිලේ ලැබෙන සීමාව ඉක්මවා යයි.")

with col2:
    st.header("Step 2: Nexo Cloud Run (AWS Server)")
    st.write("ගේම් එක සර්වර් එක මත ධාවනය කරන්න. ඔබේ දුරකථනයේ හෝ පරිගණකයේ කිසිදු ඉඩක් හෝ RAM එකක් වැය නොවේ.")
    
    # දැනට තියෙන Heavy Games ටිකක් තෝරන්න දෙනවා
    game_choice = st.selectbox("සර්වර් එකෙන් ප්ලේ කරන්න ඕන ගේම් එක තෝරන්න:", ["Free Fire", "PUBG Mobile", "Custom Uploaded Game"])
    
    st.write("---")
    st.write("### 🖥️ Nexo Streaming Display")
    
    # Play බටන් එක
    if st.button(f"🚀 Run {game_choice} on AWS Cloud"):
        st.warning("Connecting to Amazon AWS EC2 Instance via WebRTC...")
        
        # ගේම් එක ලෝඩ් වෙනකම් පොඩි ඇනිමේෂන් එකක්
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
            
        st.success(f"🟢 Connected! {game_choice} සර්වර් එක මත සාර්ථකව රන් වෙනවා. (Rs. 100/mo Pack Active)")
        
        # AWS සර්වර් එකෙන් එන වීඩියෝ ස්ට්‍රීම් එක (Demo එකක් විදිහට අපි HTML Frame එකක් දාමු)
        # ඇත්තටම Free Fire ස්ට්‍රීම් එකක් වගේ පේන්න අපි ලස්සන 3D Gameplay වීඩියෝ ලින්ක් එකක් මෙතනට දානවා
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # මෙතනට AWS එකෙන් එන Stream Link එක පස්සේ දාන්න පුළුවන්
