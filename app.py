import streamlit as st
import requests
import json
import re
import time
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexo AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* ── Root ── */
:root {
    --bg:        #080c14;
    --bg2:       #0d1322;
    --bg3:       #121929;
    --border:    #1e2d47;
    --accent:    #00d4ff;
    --accent2:   #7c3aed;
    --accent3:   #10b981;
    --text:      #e2e8f0;
    --muted:     #64748b;
    --code-bg:   #060a10;
    --glow:      0 0 20px rgba(0,212,255,0.15);
    --glow2:     0 0 40px rgba(124,58,237,0.12);
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp {
    background: 
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(124,58,237,0.07) 0%, transparent 60%),
        var(--bg);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ── Logo block ── */
.nexo-logo {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
}

.nexo-logo .hex {
    font-size: 28px;
    line-height: 1;
    display: inline-block;
    animation: spin-slow 8s linear infinite;
}

@keyframes spin-slow {
    0%   { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}

.nexo-logo h1 {
    font-family: 'Syne', sans-serif;
    font-size: 24px;
    font-weight: 800;
    margin: 6px 0 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.nexo-logo p {
    font-size: 11px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em;
    margin: 0;
}

/* ── Mode selector ── */
.mode-label {
    font-size: 10px;
    font-family: 'Space Mono', monospace;
    color: var(--muted);
    letter-spacing: 0.15em;
    padding: 16px 24px 8px;
    text-transform: uppercase;
}

.mode-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px 24px;
    cursor: pointer;
    transition: all 0.2s;
    border-left: 3px solid transparent;
    font-size: 14px;
    font-weight: 600;
    color: var(--muted);
    text-decoration: none;
}

.mode-btn:hover {
    background: rgba(0,212,255,0.04);
    color: var(--text);
}

.mode-btn.active {
    border-left-color: var(--accent);
    background: rgba(0,212,255,0.06);
    color: var(--accent);
}

.mode-btn .icon { font-size: 16px; }

/* ── Sidebar stats ── */
.sidebar-stats {
    padding: 16px 24px;
    border-top: 1px solid var(--border);
    margin-top: auto;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    font-size: 12px;
}

.stat-label { color: var(--muted); font-family: 'Space Mono', monospace; }
.stat-value { color: var(--accent); font-family: 'Space Mono', monospace; font-weight: 700; }

/* ── Header strip ── */
.nexo-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
}

.nexo-header .mode-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.badge-normal {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    color: var(--accent3);
}

.badge-coding {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent);
}

.badge-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}

.dot-normal { background: var(--accent3); box-shadow: 0 0 6px var(--accent3); }
.dot-coding { background: var(--accent);  box-shadow: 0 0 6px var(--accent); }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.85); }
}

/* ── Chat messages ── */
.msg-wrap {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 8px 0;
}

.msg {
    display: flex;
    gap: 14px;
    animation: fadeSlide 0.3s ease-out;
}

@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-avatar {
    width: 34px; height: 34px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
    font-family: 'Space Mono', monospace;
}

.avatar-user {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa;
}

.avatar-ai {
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.25);
    color: var(--accent);
}

.msg-body { flex: 1; min-width: 0; }

.msg-meta {
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    color: var(--muted);
    margin-bottom: 6px;
    display: flex; align-items: center; gap: 8px;
}

.msg-meta .role { font-weight: 700; color: var(--text); }

.msg-content {
    font-size: 14.5px;
    line-height: 1.75;
    color: var(--text);
}

.msg-content p { margin: 0 0 12px; }
.msg-content p:last-child { margin-bottom: 0; }

/* ── Code blocks ── */
.msg-content pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    overflow-x: auto;
    margin: 14px 0;
    position: relative;
}

.msg-content code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.12);
    padding: 2px 6px;
    border-radius: 4px;
    color: var(--accent);
}

.msg-content pre code {
    background: none;
    border: none;
    padding: 0;
    color: #a8d8f0;
    font-size: 13px;
}

/* ── Code header ── */
.code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px 0;
    margin-bottom: -6px;
}

.code-lang {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: rgba(0,212,255,0.08);
    padding: 3px 8px;
    border-radius: 4px;
}

/* ── Thinking block ── */
.thinking-block {
    background: rgba(124,58,237,0.05);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 10px;
    padding: 14px 16px;
    margin: 12px 0;
    font-size: 13px;
    font-family: 'JetBrains Mono', monospace;
    color: #c4b5fd;
    line-height: 1.6;
}

.thinking-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--accent2);
    margin-bottom: 8px;
    font-weight: 700;
}

/* ── File creation blocks (coding mode) ── */
.file-create-block {
    background: rgba(16,185,129,0.04);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--accent3);
    animation: fadeSlide 0.3s ease-out;
}

.file-create-block .fc-icon { font-size: 15px; }
.file-create-block .fc-name { font-weight: 600; }
.file-create-block .fc-why { color: var(--muted); font-size: 12px; margin-left: auto; }

/* ── Input area ── */
.input-wrap {
    position: sticky;
    bottom: 0;
    padding: 20px 0 12px;
    background: linear-gradient(0deg, var(--bg) 80%, transparent);
}

/* ── Streamlit overrides ── */
.stTextArea textarea {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--glow) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), #0099cc) !important;
    color: #080c14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 0 24px rgba(0,212,255,0.35) !important;
}

.stSelectbox > div > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

.stTextInput input {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: var(--glow) !important;
}

/* labels */
label, .stSelectbox label, .stTextInput label, .stTextArea label {
    color: var(--muted) !important;
    font-size: 11px !important;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* radio */
.stRadio > div { gap: 8px; }
.stRadio > div > label {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* divider */
hr { border-color: var(--border) !important; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* Alert / info */
.stAlert { border-radius: 10px !important; }

/* Welcome card */
.welcome-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin: 40px auto;
    max-width: 560px;
}

.welcome-card .hex-big {
    font-size: 52px;
    display: block;
    margin-bottom: 16px;
    animation: spin-slow 8s linear infinite;
}

.welcome-card h2 {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 8px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.welcome-card p {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 24px;
}

.welcome-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
}

.chip {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 12px;
    font-family: 'Space Mono', monospace;
    color: var(--accent);
}

/* Coding mode step indicator */
.step-indicator {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 14px 0;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    animation: fadeSlide 0.3s ease-out;
}

.step-num {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: var(--accent);
    font-size: 10px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-weight: 700;
}

.step-item.active { color: var(--text); }
.step-item.active .step-num {
    background: var(--accent);
    color: var(--bg);
}
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────
GROQ_API_URL  = "https://api.groq.com/openai/v1/chat/completions"
MODEL         = "meta-llama/llama-4-scout-17b-16e-instruct"
TEAM_NAME     = "Nexo Mind"

SYSTEM_NORMAL = f"""You are Nexo AI, an intelligent and friendly assistant created by {TEAM_NAME}.

You are knowledgeable, concise, and helpful across all topics — from general knowledge to technical explanations. You have a warm, professional personality. You remember that you were built by {TEAM_NAME} and always mention this proudly if asked about your origins.

Guidelines:
- Be friendly, clear, and precise in your responses
- Use markdown formatting where appropriate
- Be honest about your limitations
- Keep responses focused and useful"""

SYSTEM_CODING = f"""You are Nexo AI, an elite coding assistant created by {TEAM_NAME}. You are an expert software engineer who writes clean, production-grade code.

When given a coding task, follow this EXACT process and show each step clearly:

## Your Process:

**Step 1 — Understand** 🔍
Briefly analyze what the user wants. Identify: language, framework, goal, edge cases.

**Step 2 — Plan** 📋
List the files you will create/modify and why. Format:
- `filename.ext` — purpose of this file

**Step 3 — Create** ⚡
Write the complete, working code for each file. Include:
- Full implementations (no placeholders)
- Comments for complex logic
- Error handling
- Best practices for the language/framework

**Step 4 — Explain** 💡
After the code: brief explanation of key decisions, how to run it, and any important notes.

You built by {TEAM_NAME}. Always write code as if it's going into production. Be thorough, precise, and explain your reasoning clearly. Never write incomplete or placeholder code."""

# ── Session state ────────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "mode"          not in st.session_state: st.session_state.mode          = "normal"
if "api_key"       not in st.session_state: st.session_state.api_key       = ""
if "msg_count"     not in st.session_state: st.session_state.msg_count     = 0
if "token_count"   not in st.session_state: st.session_state.token_count   = 0
# Fix 1 & 2: input_key increments to clear text area; pending_send carries the
# user's message across the rerun that clears the box — no infinite loop.
if "input_key"     not in st.session_state: st.session_state.input_key     = 0
if "pending_send"  not in st.session_state: st.session_state.pending_send  = None

# ── Helpers ──────────────────────────────────────────────────────────────────
def call_groq(messages: list, system_prompt: str, api_key: str) -> dict:
    """Call Groq API and return response dict."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "temperature": 0.7,
        "max_tokens": 4096,
        "stream": False,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()


def extract_files_from_response(text: str) -> list:
    """Extract file creation mentions from coding responses."""
    files = []
    # Match patterns like `filename.ext`
    pattern = r'`([a-zA-Z0-9_\-/]+\.[a-zA-Z0-9]+)`\s*[—–-]\s*([^\n]+)'
    matches = re.findall(pattern, text)
    for fname, reason in matches:
        files.append({"name": fname, "reason": reason.strip()})
    return files


def render_message(role: str, content: str, timestamp: str = ""):
    """Render a single chat message."""
    if role == "user":
        avatar_class = "avatar-user"
        avatar_icon  = "U"
        role_label   = "You"
    else:
        avatar_class = "avatar-ai"
        avatar_icon  = "⬡"
        role_label   = "Nexo AI"

    ts = timestamp or datetime.now().strftime("%H:%M")

    # Detect file creation blocks for coding mode
    files = []
    if role == "assistant" and st.session_state.mode == "coding":
        files = extract_files_from_response(content)

    st.markdown(f"""
    <div class="msg">
      <div class="msg-avatar {avatar_class}">{avatar_icon}</div>
      <div class="msg-body">
        <div class="msg-meta">
          <span class="role">{role_label}</span>
          <span>{ts}</span>
        </div>
    """, unsafe_allow_html=True)

    # File creation indicators (coding mode)
    if files:
        for f in files:
            st.markdown(f"""
            <div class="file-create-block">
              <span class="fc-icon">📄</span>
              <span class="fc-name">{f['name']}</span>
              <span class="fc-why">{f['reason']}</span>
            </div>
            """, unsafe_allow_html=True)

    # Render actual content
    st.markdown(content)
    st.markdown("</div></div>", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="nexo-logo">
      <span class="hex">⬡</span>
      <h1>Nexo AI</h1>
      <p>POWERED BY NEXO MIND · LLAMA 4 SCOUT</p>
    </div>
    """, unsafe_allow_html=True)

    # Mode selector
    st.markdown('<div class="mode-label">Select Mode</div>', unsafe_allow_html=True)
    mode = st.radio(
        "mode_radio",
        options=["💬  Normal Mode", "💻  Coding Mode"],
        label_visibility="collapsed",
        key="mode_radio_widget",
    )
    st.session_state.mode = "normal" if "Normal" in mode else "coding"

    st.divider()

    # API Key
    api_key_input = st.text_input(
        "GROQ API KEY",
        type="password",
        placeholder="gsk_...",
        value=st.session_state.api_key,
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    st.divider()

    # Model info
    st.markdown("""
    <div class="mode-label">Model Info</div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding:0 0 12px;">
      <div class="stat-row">
        <span class="stat-label">Model</span>
        <span class="stat-value" style="font-size:10px;">LLaMA 4 Scout</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">Provider</span>
        <span class="stat-value">Groq</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">Messages</span>
        <span class="stat-value">{st.session_state.msg_count}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Clear chat
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.messages  = []
        st.session_state.msg_count = 0
        st.rerun()

    # Footer
    st.markdown("""
    <div style="padding:20px 0 8px; text-align:center;">
      <p style="font-size:11px; color:#334155; font-family:'Space Mono',monospace;">
        Built by Nexo Mind<br>
        <span style="color:#1e3a52;">⬡ nexo ai v1.0</span>
      </p>
    </div>
    """, unsafe_allow_html=True)


# ── Main area ─────────────────────────────────────────────────────────────────
# Header
mode_label  = "Normal Mode" if st.session_state.mode == "normal" else "Coding Mode"
badge_class = "badge-normal" if st.session_state.mode == "normal" else "badge-coding"
dot_class   = "dot-normal"  if st.session_state.mode == "normal" else "dot-coding"
mode_icon   = "💬" if st.session_state.mode == "normal" else "💻"

st.markdown(f"""
<div class="nexo-header">
  <div style="display:flex;align-items:center;gap:12px;">
    <span style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
          background:linear-gradient(90deg,#00d4ff,#7c3aed);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      Nexo AI
    </span>
    <div class="mode-badge {badge_class}">
      <div class="badge-dot {dot_class}"></div>
      {mode_icon} {mode_label}
    </div>
  </div>
  <span style="font-family:'Space Mono',monospace;font-size:11px;color:#334155;">
    meta-llama/llama-4-scout · groq
  </span>
</div>
""", unsafe_allow_html=True)

# ── Welcome screen ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    if st.session_state.mode == "normal":
        st.markdown("""
        <div class="welcome-card">
          <span class="hex-big">⬡</span>
          <h2>Hey there! I'm Nexo AI</h2>
          <p>Your intelligent companion built by <strong style="color:#00d4ff;">Nexo Mind</strong>.<br>
          Ask me anything — I'm here to help.</p>
          <div class="welcome-chips">
            <span class="chip">General Questions</span>
            <span class="chip">Research</span>
            <span class="chip">Creative Writing</span>
            <span class="chip">Analysis</span>
            <span class="chip">Brainstorming</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="welcome-card">
          <span class="hex-big">💻</span>
          <h2>Coding Mode Active</h2>
          <p>I'll analyze your request, plan the solution, create files, and explain every decision.<br>
          Built for production-grade code by <strong style="color:#00d4ff;">Nexo Mind</strong>.</p>
          <div class="welcome-chips">
            <span class="chip">Full-Stack Apps</span>
            <span class="chip">APIs</span>
            <span class="chip">Algorithms</span>
            <span class="chip">Debugging</span>
            <span class="chip">Code Review</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("ts", ""))

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("---")

placeholder = (
    "Ask me anything..." 
    if st.session_state.mode == "normal" 
    else "Describe what you want to build..."
)

col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_area(
        "MESSAGE",
        placeholder=placeholder,
        height=90,
        key="user_input",
        label_visibility="collapsed",
    )
with col2:
    send = st.button("Send ⬡", use_container_width=True)

# ── Handle send ───────────────────────────────────────────────────────────────
if send and user_input.strip():
    if not st.session_state.api_key:
        st.error("⚠️  Please enter your Groq API key in the sidebar.")
        st.stop()

    ts = datetime.now().strftime("%H:%M")

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip(),
        "ts": ts,
    })
    st.session_state.msg_count += 1

    # Build API messages (last 20 for context)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[-20:]
    ]

    system_prompt = SYSTEM_CODING if st.session_state.mode == "coding" else SYSTEM_NORMAL

    # Stream-style UX with spinner
    with st.spinner("Nexo AI is thinking..."):
        try:
            result = call_groq(api_messages, system_prompt, st.session_state.api_key)
            reply  = result["choices"][0]["message"]["content"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply,
                "ts": datetime.now().strftime("%H:%M"),
            })
            st.session_state.msg_count += 1

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            if status == 401:
                st.error("❌  Invalid API key. Please check your Groq API key.")
            elif status == 429:
                st.error("⚠️  Rate limit hit. Please wait a moment and try again.")
            else:
                st.error(f"❌  API error {status}: {e}")
        except Exception as e:
            st.error(f"❌  Error: {str(e)}")

    st.rerun()
