                        import streamlit as st
import requests
import json
import time
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nexo AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Exo+2:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300&display=swap');

/* ── Reset & Root ─────────────────────────────── */
:root {
    --bg-deep:      #070711;
    --bg-panel:     #0d0d1f;
    --bg-card:      #11112a;
    --bg-hover:     #161630;
    --accent-blue:  #4f8ef7;
    --accent-purple:#8b5cf6;
    --accent-violet:#a78bfa;
    --accent-cyan:  #22d3ee;
    --text-primary: #e8eaf6;
    --text-secondary:#9399b2;
    --text-muted:   #555878;
    --border:       rgba(79,142,247,0.15);
    --border-bright:rgba(79,142,247,0.35);
    --glow-blue:    rgba(79,142,247,0.25);
    --glow-purple:  rgba(139,92,246,0.2);
    --sidebar-w:    260px;
    --right-w:      300px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"],
[data-testid="stDecoration"] { display: none !important; }

/* Remove default padding */
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Scrollbar ────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 2px; }

/* ── Layout Shell ─────────────────────────────── */
.nexo-shell {
    display: grid;
    grid-template-columns: var(--sidebar-w) 1fr var(--right-w);
    height: 100vh;
    overflow: hidden;
    position: relative;
}

/* ── LEFT SIDEBAR ─────────────────────────────── */
.nexo-sidebar {
    background: var(--bg-panel);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 20px 14px;
    gap: 6px;
    overflow-y: auto;
    overflow-x: hidden;
    transition: transform 0.35s cubic-bezier(.4,0,.2,1);
}

.nexo-sidebar.hidden {
    transform: translateX(calc(-1 * var(--sidebar-w)));
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: var(--sidebar-w);
    z-index: 50;
}

/* Brand */
.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 18px;
    padding: 0 6px;
}
.brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 16px; color: white;
    font-family: 'Orbitron', monospace;
    box-shadow: 0 0 16px var(--glow-blue);
}
.brand-name {
    font-family: 'Orbitron', monospace;
    font-weight: 700; font-size: 15px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}
.brand-name span { color: var(--accent-violet); -webkit-text-fill-color: var(--accent-violet); }

/* New Chat btn */
.new-chat-btn {
    display: flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, rgba(79,142,247,0.15), rgba(139,92,246,0.15));
    border: 1px solid var(--border-bright);
    border-radius: 12px;
    padding: 10px 14px;
    cursor: pointer;
    color: var(--text-primary);
    font-family: 'Exo 2', sans-serif;
    font-size: 13px; font-weight: 500;
    width: 100%;
    justify-content: space-between;
    transition: all 0.2s;
    margin-bottom: 10px;
}
.new-chat-btn:hover {
    background: linear-gradient(135deg, rgba(79,142,247,0.25), rgba(139,92,246,0.25));
    box-shadow: 0 0 20px var(--glow-blue);
}

/* Nav items */
.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 12px;
    border-radius: 10px;
    cursor: pointer;
    color: var(--text-secondary);
    font-size: 13px; font-weight: 400;
    transition: all 0.2s;
    border: 1px solid transparent;
}
.nav-item:hover { background: var(--bg-hover); color: var(--text-primary); }
.nav-item.active {
    background: linear-gradient(135deg, rgba(79,142,247,0.18), rgba(139,92,246,0.12));
    border-color: var(--border-bright);
    color: var(--accent-blue);
}
.nav-badge {
    margin-left: auto;
    background: var(--accent-purple);
    color: white; font-size: 10px;
    border-radius: 20px; padding: 2px 7px;
    font-weight: 700;
}

/* Section label */
.section-label {
    font-size: 9px; letter-spacing: 2px;
    color: var(--text-muted); text-transform: uppercase;
    padding: 10px 12px 4px;
    font-weight: 600;
}

/* Recent chat items */
.recent-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
}
.recent-item:hover { background: var(--bg-hover); }
.recent-item-title { font-size: 12px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px; }
.recent-item-time { font-size: 10px; color: var(--text-muted); white-space: nowrap; }
.recent-item.active .recent-item-title { color: var(--text-primary); }

/* User profile */
.user-profile {
    margin-top: auto;
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid var(--border);
    cursor: pointer;
    transition: background 0.2s;
}
.user-profile:hover { background: var(--bg-hover); }
.user-avatar {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.user-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.user-badge { font-size: 10px; color: var(--accent-violet); font-weight: 500; }
.user-more { margin-left: auto; color: var(--text-muted); font-size: 16px; }

/* Divider */
.sidebar-divider { height: 1px; background: var(--border); margin: 8px 0; }

/* ── CENTER CHAT AREA ──────────────────────────── */
.nexo-center {
    display: flex;
    flex-direction: column;
    background: var(--bg-deep);
    position: relative;
    overflow: hidden;
}

/* Hero banner */
.hero-banner {
    position: relative;
    min-height: 260px;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
}
.hero-bg {
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 70% 80% at 50% 120%, rgba(139,92,246,0.35) 0%, transparent 70%),
        radial-gradient(ellipse 50% 60% at 30% 20%, rgba(79,142,247,0.15) 0%, transparent 60%),
        linear-gradient(180deg, #0a0a20 0%, #100b28 60%, #0d0d1f 100%);
}
/* Animated mountain silhouette */
.hero-mountains {
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 120px;
    background:
        linear-gradient(180deg, transparent 0%, rgba(7,7,17,0.8) 100%);
}
.hero-orb {
    position: relative; z-index: 2;
    text-align: center;
}
.hero-orb-img {
    width: 90px; height: 90px;
    margin: 0 auto 18px;
    background: conic-gradient(from 0deg, var(--accent-blue), var(--accent-purple), var(--accent-cyan), var(--accent-blue));
    border-radius: 50%;
    animation: orb-spin 8s linear infinite;
    box-shadow:
        0 0 40px var(--glow-purple),
        0 0 80px rgba(79,142,247,0.15),
        inset 0 0 30px rgba(0,0,0,0.5);
    display: flex; align-items: center; justify-content: center;
}
.hero-orb-inner {
    width: 72px; height: 72px;
    background: var(--bg-deep);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', monospace;
    font-size: 22px; font-weight: 900;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
@keyframes orb-spin {
    from { filter: hue-rotate(0deg) drop-shadow(0 0 20px var(--accent-purple)); }
    to   { filter: hue-rotate(360deg) drop-shadow(0 0 20px var(--accent-blue)); }
}
.hero-greeting {
    font-size: 22px; font-weight: 600;
    color: var(--text-primary);
    line-height: 1.3;
    text-shadow: 0 0 40px rgba(139,92,246,0.4);
}
.hero-greeting .nexo-highlight {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Chat scroll area */
.chat-scroll {
    flex: 1;
    overflow-y: auto;
    padding: 16px 28px;
    display: flex;
    flex-direction: column;
    gap: 14px;
}

/* Messages */
.msg-user {
    align-self: flex-end;
    max-width: 65%;
    background: linear-gradient(135deg, rgba(79,142,247,0.2), rgba(139,92,246,0.2));
    border: 1px solid var(--border-bright);
    border-radius: 18px 18px 4px 18px;
    padding: 11px 16px;
    font-size: 13px; line-height: 1.6;
    color: var(--text-primary);
    position: relative;
}
.msg-user-meta {
    font-size: 10px; color: var(--text-muted);
    text-align: right; margin-top: 6px;
}

.msg-ai-wrap {
    display: flex; gap: 10px; align-items: flex-start;
    max-width: 78%;
}
.msg-ai-avatar {
    width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', monospace; font-weight: 900; font-size: 11px; color: white;
    box-shadow: 0 0 12px var(--glow-blue);
}
.msg-ai-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px 18px 18px 18px;
    padding: 13px 16px;
    font-size: 13px; line-height: 1.75;
    color: var(--text-primary);
    flex: 1;
}
.msg-ai-meta {
    font-size: 10px; color: var(--text-muted);
    margin-top: 8px; display: flex; justify-content: space-between;
    align-items: center;
}

/* Suggestion chips */
.suggestion-row {
    display: flex; gap: 8px; flex-wrap: wrap;
    padding: 0 28px 14px;
}
.suggestion-chip {
    display: flex; align-items: center; gap: 6px;
    background: rgba(13,13,31,0.8);
    border: 1px solid var(--border-bright);
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 12px; color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.suggestion-chip:hover {
    background: rgba(79,142,247,0.12);
    color: var(--accent-blue);
    border-color: var(--accent-blue);
    box-shadow: 0 0 12px var(--glow-blue);
}

/* ── Input bar ─────────────────────────────────── */
.input-bar {
    padding: 14px 24px 18px;
    border-top: 1px solid var(--border);
    background: var(--bg-panel);
    flex-shrink: 0;
}
.input-wrap {
    display: flex; align-items: center; gap: 10px;
    background: var(--bg-card);
    border: 1px solid var(--border-bright);
    border-radius: 16px;
    padding: 8px 12px 8px 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.input-wrap:focus-within {
    border-color: var(--accent-blue);
    box-shadow: 0 0 20px var(--glow-blue);
}
.input-icons { display: flex; gap: 8px; }
.input-icon {
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px; cursor: pointer;
    color: var(--text-muted); font-size: 14px;
    transition: all 0.15s;
}
.input-icon:hover { background: var(--bg-hover); color: var(--text-secondary); }
.send-btn {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; flex-shrink: 0;
    box-shadow: 0 0 14px var(--glow-blue);
    transition: all 0.2s;
    border: none;
    color: white; font-size: 15px;
}
.send-btn:hover { box-shadow: 0 0 24px var(--glow-blue); transform: scale(1.08); }

/* ── RIGHT PANEL ──────────────────────────────── */
.nexo-right {
    background: var(--bg-panel);
    border-left: 1px solid var(--border);
    display: flex; flex-direction: column;
    padding: 20px 18px;
    gap: 16px;
    overflow-y: auto;
}

/* Right panel header */
.right-header {
    display: flex; align-items: center; justify-content: space-between;
}
.right-title {
    font-family: 'Orbitron', monospace;
    font-size: 13px; font-weight: 700; letter-spacing: 2px;
    color: var(--text-primary);
}
.version-badge {
    background: linear-gradient(135deg, rgba(79,142,247,0.2), rgba(139,92,246,0.2));
    border: 1px solid var(--border-bright);
    border-radius: 20px; padding: 3px 10px;
    font-size: 10px; font-weight: 600;
    color: var(--accent-blue); letter-spacing: 0.5px;
}

/* AI Profile card */
.ai-profile {
    display: flex; flex-direction: column; align-items: center;
    text-align: center; gap: 8px;
}
.ai-avatar {
    width: 80px; height: 80px;
    background: conic-gradient(from 0deg, var(--accent-blue), var(--accent-purple), var(--accent-cyan), var(--accent-blue));
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    animation: orb-spin 10s linear infinite;
    box-shadow: 0 0 30px var(--glow-purple);
}
.ai-avatar-inner {
    width: 64px; height: 64px;
    background: var(--bg-panel);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Orbitron', monospace; font-weight: 900; font-size: 18px;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-violet));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.ai-name { font-size: 15px; font-weight: 700; color: var(--text-primary); }
.ai-desc { font-size: 12px; color: var(--text-secondary); line-height: 1.5; }

/* Capabilities */
.cap-section-title {
    font-size: 9px; letter-spacing: 2px;
    color: var(--text-muted); text-transform: uppercase;
    font-weight: 700; margin-bottom: 6px;
}
.cap-list { display: flex; flex-direction: column; gap: 6px; }
.cap-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-size: 12px; color: var(--text-secondary);
    transition: all 0.2s;
}
.cap-item:hover { border-color: var(--border-bright); color: var(--text-primary); }
.cap-icon { font-size: 13px; }

/* Usage card */
.usage-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
}
.usage-title { font-size: 9px; letter-spacing: 2px; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 10px; }
.usage-num { font-size: 26px; font-weight: 700; color: var(--text-primary); font-family: 'Orbitron', monospace; }
.usage-label { font-size: 11px; color: var(--text-muted); margin-bottom: 8px; }
.usage-bar-bg {
    height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px;
    overflow: hidden;
}
.usage-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
    border-radius: 2px;
    transition: width 0.5s ease;
    box-shadow: 0 0 8px var(--glow-blue);
}
.usage-pct { font-size: 11px; color: var(--text-secondary); text-align: right; margin-top: 4px; }

/* Pro upgrade card */
.pro-card {
    background: linear-gradient(135deg, rgba(79,142,247,0.08), rgba(139,92,246,0.12));
    border: 1px solid var(--border-bright);
    border-radius: 12px;
    padding: 14px;
}
.pro-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.pro-crown { font-size: 16px; }
.pro-title { font-size: 14px; font-weight: 700; color: var(--text-primary); }
.pro-desc { font-size: 11px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px; }
.pro-btn {
    width: 100%;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
    border: none; border-radius: 8px;
    padding: 9px;
    color: white; font-size: 12px; font-weight: 600;
    cursor: pointer; font-family: 'Exo 2', sans-serif;
    transition: all 0.2s;
    box-shadow: 0 0 16px var(--glow-blue);
}
.pro-btn:hover { box-shadow: 0 0 28px var(--glow-blue); transform: translateY(-1px); }

/* ── HAMBURGER + SIDEBAR TOGGLE ────────────────── */
.hamburger-btn {
    position: fixed;
    top: 18px; left: 14px;
    z-index: 100;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 8px;
    cursor: pointer;
    display: flex; flex-direction: column; gap: 4px;
    transition: all 0.2s;
    display: none; /* shown via JS when sidebar hidden */
}
.hamburger-btn:hover { border-color: var(--accent-blue); }
.ham-line {
    width: 18px; height: 2px;
    background: var(--text-secondary);
    border-radius: 1px;
    transition: all 0.2s;
}

/* Typing indicator */
.typing-indicator {
    display: flex; gap: 4px; align-items: center; padding: 4px 0;
}
.typing-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent-purple);
    animation: bounce 1.2s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
    30% { transform: translateY(-6px); opacity: 1; }
}

/* ── Streamlit widget overrides ────────────────── */
/* Text input */
[data-testid="stTextInput"] > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    color: var(--text-primary) !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 13px !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    caret-color: var(--accent-blue);
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-muted) !important; }

/* Buttons */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple)) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 36px !important; height: 36px !important;
    padding: 0 !important;
    font-size: 16px !important;
    color: white !important;
    box-shadow: 0 0 14px var(--glow-blue) !important;
    transition: all 0.2s !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 26px var(--glow-blue) !important;
    transform: scale(1.08) !important;
}

/* Columns */
[data-testid="stHorizontalBlock"] { gap: 0 !important; }

/* Spinner */
[data-testid="stSpinner"] { color: var(--accent-purple) !important; }

/* Selectbox / API key input */
[data-testid="stTextInput"].api-input > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 10px !important;
    padding: 4px 10px !important;
}

/* Sidebar toggle pill */
.sidebar-toggle-pill {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    left: -12px;
    width: 24px; height: 48px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px 0 0 12px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 10; font-size: 10px;
    color: var(--text-muted);
    transition: all 0.2s;
}

/* Mobile overlay */
.overlay {
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 40;
}
.overlay.active { display: block; }

/* Fade-in animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-user, .msg-ai-wrap { animation: fadeUp 0.3s ease; }

/* Right panel divider */
.right-divider { height: 1px; background: var(--border); }

/* Scrollable right panel sections */
.right-scroll-inner { display: flex; flex-direction: column; gap: 14px; }

/* Custom checkbox for API key visibility */
.api-key-row {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 10px;
}
.api-key-label {
    font-size: 11px; color: var(--text-secondary); font-weight: 500;
}

/* Model selector */
.model-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(79,142,247,0.1);
    border: 1px solid var(--border-bright);
    border-radius: 20px; padding: 4px 12px;
    font-size: 11px; color: var(--accent-blue);
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ─── Load API Key from Streamlit Secrets ───────────────────────────────────────
def get_api_key() -> str:
    """Secrets වලින් API key load කරනවා. නැත්නම් empty string."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        return ""

GROQ_API_KEY = get_api_key()

# ─── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "typing" not in st.session_state:
    st.session_state.typing = False
if "suggestion_clicked" not in st.session_state:
    st.session_state.suggestion_clicked = ""


# ─── Groq API Call ─────────────────────────────────────────────────────────────
def call_groq(api_key: str, messages: list) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Nexo, an advanced AI assistant. Be helpful, concise, and insightful. "
                    "Format responses clearly. Be friendly but professional."
                )
            }
        ] + messages,
        "max_tokens": 1024,
        "temperature": 0.7,
        "stream": False,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 401:
            return "❌ Invalid API key. Please check your Groq API key."
        elif resp.status_code == 429:
            return "⏳ Rate limit reached. Please wait a moment and try again."
        else:
            return f"❌ API Error ({resp.status_code}): {str(e)}"
    except Exception as e:
        return f"❌ Connection error: {str(e)}"


def get_time():
    return datetime.now().strftime("%I:%M %p")


# ─── Recent chats mock data ─────────────────────────────────────────────────────
recent_chats = []
if st.session_state.messages:
    # Build from actual session
    first_user = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), None)
    if first_user:
        recent_chats.append({"title": first_user[:22] + "...", "time": "Now", "active": True})

recent_chats += [
    {"title": "Python Code Helper", "time": "Yesterday", "active": False},
    {"title": "The Future of AI",   "time": "May 22",    "active": False},
    {"title": "Create a Sci-fi Story","time": "May 21",  "active": False},
    {"title": "Explain Black Holes", "time": "May 18",   "active": False},
]


# ─── Sidebar toggle callback ────────────────────────────────────────────────────
def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open


# ─────────────────────────────────────────────────────────────────────────────
#  RENDER
# ─────────────────────────────────────────────────────────────────────────────

# We use three st.columns to simulate the 3-panel layout
sidebar_open = st.session_state.sidebar_open

# Column widths
if sidebar_open:
    col_ratios = [2.2, 5.5, 2.5]
else:
    col_ratios = [0.001, 7.5, 2.5]

left_col, center_col, right_col = st.columns(col_ratios, gap="small")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with left_col:
    if sidebar_open:
        st.markdown("""
        <div class="nexo-sidebar">
          <!-- Brand -->
          <div class="brand">
            <div class="brand-icon">N</div>
            <div class="brand-name">nexo <span>ai</span></div>
          </div>

          <!-- New Chat -->
          <button class="new-chat-btn">
            <span>＋ &nbsp;New Chat</span>
            <span style="opacity:.5;font-size:16px">✦</span>
          </button>

          <!-- Nav -->
          <div class="nav-item"><span>⌂</span> Home</div>
          <div class="nav-item active">
            <span>💬</span> Chats
            <span class="nav-badge">12</span>
          </div>
          <div class="nav-item"><span>◎</span> Discover</div>
          <div class="nav-item"><span>✦</span> Generate</div>
          <div class="nav-item"><span>📁</span> Library</div>
          <div class="nav-item"><span>⊙</span> Memory</div>
          <div class="nav-item"><span>⚙</span> Settings</div>

          <div class="sidebar-divider"></div>

          <!-- Recent chats -->
          <div class="section-label">Recent Chats</div>
        """, unsafe_allow_html=True)

        for ch in recent_chats[:5]:
            active_cls = "active" if ch["active"] else ""
            st.markdown(f"""
            <div class="recent-item {active_cls}">
              <span class="recent-item-title">{ch['title']}</span>
              <span class="recent-item-time">{ch['time']}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
          <!-- User -->
          <div class="sidebar-divider" style="margin-top:auto"></div>
          <div class="user-profile">
            <div class="user-avatar">🤖</div>
            <div>
              <div class="user-name">Nexo User</div>
              <div class="user-badge">Pro</div>
            </div>
            <div class="user-more">···</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Collapsed: show hamburger-style 3-line toggle
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("☰", key="open_sidebar"):
            toggle_sidebar()
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# CENTER CHAT
# ══════════════════════════════════════════════════════════════════════════════
with center_col:

    # Top bar with sidebar toggle (always visible)
    topbar_left, topbar_mid, topbar_right = st.columns([1, 8, 1])
    with topbar_left:
        if sidebar_open:
            if st.button("☰", key="close_sidebar", help="Toggle sidebar"):
                toggle_sidebar()
                st.rerun()
        else:
            if st.button("☰", key="open_sb2", help="Open sidebar"):
                toggle_sidebar()
                st.rerun()

    # ── Hero Banner ──
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-bg"></div>
      <div class="hero-mountains"></div>
      <div class="hero-orb">
        <div class="hero-orb-img">
          <div style="width:72px;height:72px;background:var(--bg-deep);border-radius:50%;
                      display:flex;align-items:center;justify-content:center;
                      font-family:'Orbitron',monospace;font-size:20px;font-weight:900;
                      background:linear-gradient(135deg,#4f8ef7,#8b5cf6);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">N</div>
        </div>
        <div class="hero-greeting">
          👋 Hello, <span class="nexo-highlight">Nexo</span> here.<br>
          How can I help you today?
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Chat messages ──
    chat_html = '<div class="chat-scroll" id="chat-scroll">'

    for msg in st.session_state.messages:
        ts = msg.get("time", get_time())
        if msg["role"] == "user":
            content_escaped = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
            chat_html += f"""
            <div class="msg-user">
              {content_escaped}
              <div class="msg-user-meta">{ts} ✓✓</div>
            </div>"""
        else:
            content_escaped = msg["content"].replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            chat_html += f"""
            <div class="msg-ai-wrap">
              <div class="msg-ai-avatar">N</div>
              <div class="msg-ai-bubble">
                {content_escaped}
                <div class="msg-ai-meta">
                  <span>{ts}</span>
                  <span title="Copy">⧉</span>
                </div>
              </div>
            </div>"""

    if st.session_state.typing:
        chat_html += """
        <div class="msg-ai-wrap">
          <div class="msg-ai-avatar">N</div>
          <div class="msg-ai-bubble">
            <div class="typing-indicator">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
          </div>
        </div>"""

    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Auto-scroll JS
    st.markdown("""
    <script>
    const el = document.getElementById('chat-scroll');
    if (el) el.scrollTop = el.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    # ── Suggestion chips ──
    if not st.session_state.messages:
        st.markdown("""
        <div class="suggestion-row">
          <div class="suggestion-chip" onclick="document.querySelector('input').value='Explain quantum computing'">Explain further →</div>
          <div class="suggestion-chip" onclick="">Give real-world example →</div>
          <div class="suggestion-chip" onclick="">How does it work? →</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Input bar ──
    st.markdown("""
    <div class="input-bar">
      <div class="input-wrap">
    """, unsafe_allow_html=True)

    inp_left, inp_mid, inp_right = st.columns([0.5, 9, 0.8])

    with inp_left:
        st.markdown("""
        <div class="input-icons" style="padding-top:4px">
          <div class="input-icon">📎</div>
          <div class="input-icon">🖼</div>
          <div class="input-icon">&lt;/&gt;</div>
          <div class="input-icon">🎤</div>
        </div>
        """, unsafe_allow_html=True)

    with inp_mid:
        user_input = st.text_input(
            label="",
            placeholder="Message Nexo...",
            key="user_msg",
            label_visibility="collapsed",
        )

    with inp_right:
        send = st.button("➤", key="send_btn")

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Handle send ──
    if (send or (user_input and user_input != st.session_state.get("last_input", ""))) and user_input.strip():
        st.session_state.last_input = user_input
        api_key = GROQ_API_KEY

        if not api_key:
            st.error("⚠️ API key not configured. Please add GROQ_API_KEY to Streamlit secrets.")
        else:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input.strip(),
                "time": get_time(),
            })
            st.session_state.usage_count += 1

            # Call API
            groq_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            with st.spinner(""):
                response = call_groq(api_key, groq_messages)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "time": get_time(),
            })
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT PANEL
# ══════════════════════════════════════════════════════════════════════════════
with right_col:
    # Header
    st.markdown("""
    <div class="nexo-right">
      <div class="right-header">
        <span class="right-title">NEXO AI</span>
        <span class="version-badge">v2.5 Pro</span>
      </div>

      <!-- AI Avatar -->
      <div class="ai-profile">
        <div class="ai-avatar">
          <div style="width:64px;height:64px;background:var(--bg-panel);border-radius:50%;
                      display:flex;align-items:center;justify-content:center;
                      font-family:'Orbitron',monospace;font-weight:900;font-size:18px;
                      background:linear-gradient(135deg,#4f8ef7,#a78bfa);
                      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">N</div>
        </div>
        <div class="ai-name">Advanced AI Assistant</div>
        <div class="ai-desc">Built to help you explore, create,<br>and understand the world better.</div>
      </div>

      <div class="right-divider"></div>
    """, unsafe_allow_html=True)

    # API Key status (secrets වලින් load වෙනවා)
    if GROQ_API_KEY:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                    background:rgba(34,211,102,0.08);border:1px solid rgba(34,211,102,0.25);
                    border-radius:10px;margin-bottom:4px;">
          <span style="font-size:11px;color:#4ade80;">●</span>
          <span style="font-size:11px;color:#9399b2;font-weight:500;">API Key Connected</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                    background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);
                    border-radius:10px;margin-bottom:4px;">
          <span style="font-size:11px;color:#f87171;">●</span>
          <span style="font-size:11px;color:#9399b2;font-weight:500;">API Key Not Set</span>
        </div>
        """, unsafe_allow_html=True)

    # Model chip
    st.markdown("""
    <div style="margin:4px 0 10px">
      <span class="model-chip">🦙 llama-4-scout-17b</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="right-divider"></div>', unsafe_allow_html=True)

    # Capabilities
    st.markdown("""
      <div class="cap-section-title">CAPABILITIES</div>
      <div class="cap-list">
        <div class="cap-item"><span class="cap-icon">💬</span> Smart Conversations</div>
        <div class="cap-item"><span class="cap-icon">✏️</span> Content Generation</div>
        <div class="cap-item"><span class="cap-icon">&lt;/&gt;</span> Code Assistance</div>
        <div class="cap-item"><span class="cap-icon">📊</span> Data Analysis</div>
        <div class="cap-item"><span class="cap-icon">🖼</span> Image Generation</div>
      </div>

      <div class="right-divider"></div>
    """, unsafe_allow_html=True)

    # Usage
    usage = st.session_state.usage_count
    max_usage = 30
    pct = min(int((usage / max_usage) * 100), 100)

    st.markdown(f"""
      <div class="usage-card">
        <div class="usage-title">USAGE TODAY</div>
        <div class="usage-num">{usage}</div>
        <div class="usage-label">Messages</div>
        <div class="usage-bar-bg">
          <div class="usage-bar-fill" style="width:{pct}%"></div>
        </div>
        <div class="usage-pct">{pct}%</div>
      </div>
    """, unsafe_allow_html=True)

    # Pro card
    st.markdown("""
      <div class="pro-card">
        <div class="pro-header">
          <span class="pro-crown">👑</span>
          <span class="pro-title">Unlock More with Pro</span>
        </div>
        <div class="pro-desc">Get unlimited access to all features and capabilities.</div>
        <button class="pro-btn">👑 Upgrade Now</button>
      </div>

      <!-- Close the nexo-right div -->
    </div>
    """, unsafe_allow_html=True)

    # Clear chat button
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", key="clear_btn", use_container_width=True):
        st.session_state.messages = []
        st.session_state.usage_count = 0
        st.rerun()
