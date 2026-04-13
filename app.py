import streamlit as st
import requests

# --- Cloudflare සැකසුම් ---
CLOUDFLARE_ACCOUNT_ID = "2974b71a6d3dab87c1216cfd085422c5"
# ඔබ එවපු අලුත්ම Token එක
CLOUDFLARE_API_TOKEN = "cfut_t4CR6D0dkwBS3ddOkoYm4c3zGXb9Yi8VEnqMCmDi3f008498"

# 1. Token එක වැඩ කරනවාදැයි පරීක්ෂා කරන Function එක (Verify Method)
def verify_token():
    verify_url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"}
    try:
        response = requests.get(verify_url, headers=headers)
        return response.json()
    except Exception as e:
        return {"success": False, "errors": [{"message": str(e)}]}

# 2. පින්තූරය සාදන Function එක
def generate_image(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"prompt": prompt}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        return f"Error {response.status_code}: {response.text}"

# --- UI කොටස ---
st.set_page_config(page_title="Alpha Private AI", page_icon="🛡️")
st.title("🛡️ Alpha Private Photo Lab")

# මුලින්ම Token එක Verify කරමු
with st.sidebar:
    st.header("System Status")
    if st.button("Check Connection 🔍"):
        status = verify_token()
        if status.get("success"):
            st.success("Token එක වැඩ කරයි! (Active)")
        else:
            st.error("Token එකේ ගැටලුවක් තියෙනවා!")
            st.json(status)

prompt_input = st.text_input("පින්තූරය ගැන ලියන්න (English):")

if st.button("Generate Image 🚀"):
    if prompt_input:
        with st.spinner("Alpha Engine වැඩ කරයි..."):
            result = generate_image(prompt_input)
            
            if isinstance(result, bytes):
                st.image(result, caption="Alpha Gen Result", use_container_width=True)
                st.success("වැඩේ සාර්ථකයි!")
            else:
                st.error("පින්තූරය සැකසීමට නොහැකි විය.")
                st.info("ඔබේ Token එකේ 'Workers AI' සඳහා Permissions තිබේදැයි බලන්න.")
    else:
        st.warning("කරුණාකර විස්තරයක් ලියන්න.")
