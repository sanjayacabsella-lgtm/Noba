import streamlit as st
from openai import OpenAI
from github import Github
import json
import os

# --- 1. CONFIGURATION & SECRETS ---
# Streamlit Secrets වලින් දත්ත ලබා ගැනීම
GITHUB_TOKEN = st.secrets["GITHUB_MODELS_TOKEN"]
REPO_NAME = st.secrets["REPO_NAME"]

# GitHub Models සඳහා OpenAI Client එක සකස් කිරීම
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
)

# --- 2. PAGE UI SETUP ---
st.set_page_config(page_title="Alpha Ultra AI v1.2", page_icon="🏎️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .stTextArea textarea { background-color: #111; color: #00ff00; border: 1px solid #333; }
    .stButton>button { background: linear-gradient(45deg, #ff4b4b, #ff8100); color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 Alpha Ultra v1.2: AI to Unreal Engine")
st.caption("Using GitHub Models (GPT-4o) + Streamlit Secrets")

# --- 3. MAIN INTERFACE ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎮 Mission Designer")
    user_prompt = st.text_area(
        "මොකක්ද වෙන්න ඕනේ? (Prompt)",
        "Example: A GTA-style police chase in a dark rainy city. 3 police cars following a black van. Add neon street lights.",
        height=200
    )

with col2:
    st.subheader("🛠️ Technical Specs")
    weather = st.selectbox("Weather", ["Sunny", "Rainy", "Foggy", "Heavy Storm"])
    time_of_day = st.select_slider("Time of Day", options=["Night", "Dawn", "Day", "Dusk"])
    spawn_density = st.number_input("Object Density", min_value=1, max_value=50, value=10)

# --- 4. THE CORE LOGIC ---
if st.button("🚀 SYNC WITH UNREAL ENGINE"):
    if not user_prompt:
        st.warning("කරුණාකර Prompt එකක් ඇතුළත් කරන්න.")
    else:
        try:
            # --- A. GPT-4o (GitHub Models) Call ---
            with st.spinner("Alpha AI විසින් Unreal Logic එක හදනවා..."):
                system_prompt = f"""
                You are a Senior UE5 Technical Artist. Output ONLY raw JSON.
                Target: Unreal Engine 5.4.
                Weather: {weather}, Time: {time_of_day}.
                
                Project Asset Mapping:
                - Police: "BP_Police_Interceptor_C"
                - Player: "BP_Player_Vehicle_C"
                - Civilian: "BP_Civ_Car_Generic_C"
                - NPC: "BP_MetaHuman_Base_C"
                
                JSON Format:
                {{
                    "mission_name": "Alpha_Generated_Level",
                    "weather_settings": {{"type": "{weather}", "time": "{time_of_day}"}},
                    "actors": [
                        {{"class": "Asset_Name", "transform": {{"loc": [x, y, z], "rot": [r, p, y]}}}}
                    ]
                }}
                """

                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    model="gpt-4o", # GitHub Models වල තියෙන model එක
                    temperature=1,
                    max_tokens=2048,
                    top_p=1
                )

                generated_json = response.choices[0].message.content
                # JSON එක පිරිසිදු කිරීම (Markdown tags අයින් කිරීම)
                if "```json" in generated_json:
                    generated_json = generated_json.split("```json")[1].split("```")[0].strip()

            # --- B. GitHub Commit Logic ---
            with st.spinner("GitHub එකට Data යවනවා..."):
                g = Github(GITHUB_TOKEN)
                repo = g.get_repo(REPO_NAME)
                file_path = "AlphaGenerated/current_mission.json"
                
                try:
                    contents = repo.get_contents(file_path)
                    repo.update_file(contents.path, "Alpha Update: Mission Gen", generated_json, contents.sha)
                    st.success("✅ GitHub Repo එක Update කරා!")
                except:
                    repo.create_file(file_path, "Alpha AI: New Mission", generated_json)
                    st.success("✅ අලුත් Mission එකක් Create කරා!")

                # Result Display
                st.balloons()
                st.subheader("📦 Generated JSON Data")
                st.json(json.loads(generated_json))

        except Exception as e:
            st.error(f"Error එකක් ආවා මචං: {str(e)}")

# --- 5. FOOTER ---
st.divider()
st.markdown("💡 **Unreal Engine එකේ කරන්න ඕන දේ:** Pull බටන් එක එබුවම `AlphaGenerated/current_mission.json` කියන ෆයිල් එක කියවන්න.")
