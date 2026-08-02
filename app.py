import os
import time
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Historic AI — Discover the World's Heritage",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64

# Function to encode local background image to base64
def get_bg_css(image_path="background.png"):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode()
        return f"linear-gradient(rgba(8, 10, 16, 0.72), rgba(8, 10, 16, 0.88)), url('data:image/png;base64,{b64_data}') center/cover no-repeat fixed"
    return "radial-gradient(circle at 50% -20%, #241b3a 0%, #0b0e14 65%)"

bg_css_value = get_bg_css("background.png")

# Apply dynamic background image style
st.markdown(f"""
<style>
.stApp {{
    background: {bg_css_value} !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f3f4f6;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Custom CSS & Animations
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Hide default headers */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ---------------- Animations ---------------- */
@keyframes goldGlow {
    0% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.4), 0 0 20px rgba(255, 215, 0, 0.2); }
    50% { text-shadow: 0 0 22px rgba(255, 215, 0, 0.85), 0 0 38px rgba(255, 215, 0, 0.55), 0 0 55px rgba(255, 165, 0, 0.35); }
    100% { text-shadow: 0 0 10px rgba(255, 215, 0, 0.4), 0 0 20px rgba(255, 215, 0, 0.2); }
}

@keyframes slideUpFade {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floatAnimation {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

@keyframes iconGlowPulse {
    0% { filter: drop-shadow(0 0 12px rgba(255, 215, 0, 0.35)); }
    50% { filter: drop-shadow(0 0 32px rgba(255, 215, 0, 0.75)); }
    100% { filter: drop-shadow(0 0 12px rgba(255, 215, 0, 0.35)); }
}

@keyframes pulseBorder {
    0% { border-color: rgba(255, 215, 0, 0.3); box-shadow: 0 0 15px rgba(255, 215, 0, 0.1); }
    50% { border-color: rgba(255, 215, 0, 0.8); box-shadow: 0 0 25px rgba(255, 215, 0, 0.3); }
    100% { border-color: rgba(255, 215, 0, 0.3); box-shadow: 0 0 15px rgba(255, 215, 0, 0.1); }
}

@keyframes cardRise {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ---------------- Hero Section ---------------- */
.hero-container {
    text-align: center;
    padding: 3rem 1rem 1.2rem 1rem;
    animation: slideUpFade 0.8s ease-out;
}

.hero-icon-wrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 110px;
    height: 110px;
    border-radius: 28px;
    background: linear-gradient(145deg, rgba(255,215,0,0.12), rgba(255,165,0,0.05));
    border: 1px solid rgba(255, 215, 0, 0.25);
    margin-bottom: 1.1rem;
    animation: floatAnimation 4.5s ease-in-out infinite;
}

.hero-icon {
    font-size: 3.6rem;
    display: inline-block;
    animation: iconGlowPulse 3.5s ease-in-out infinite;
}

.hero-title {
    font-family: 'Cinzel', serif;
    font-size: 3.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFF099 0%, #FFD700 50%, #FFA500 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: goldGlow 4s ease-in-out infinite;
    letter-spacing: 3px;
    margin-bottom: 0.4rem;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #9ca3af;
    font-weight: 400;
    max-width: 640px;
    margin: 0 auto 0.5rem auto;
    line-height: 1.55;
}

/* ---------------- Feature Cards ---------------- */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    max-width: 1050px;
    margin: 2rem auto 0.5rem auto;
    padding: 0 1rem;
}

@media (max-width: 900px) {
    .feature-grid { grid-template-columns: repeat(2, 1fr); }
}

.feature-card {
    background: rgba(22, 27, 38, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.3rem 1.2rem;
    text-align: left;
    animation: cardRise 0.6s ease-out forwards;
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: rgba(255, 215, 0, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
}

.feature-icon-badge {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: rgba(255, 215, 0, 0.1);
    border: 1px solid rgba(255, 215, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 0.7rem;
}

.feature-card h4 {
    font-size: 1rem;
    font-weight: 700;
    color: #f3f4f6;
    margin: 0 0 0.35rem 0;
}

.feature-card p {
    font-size: 0.83rem;
    color: #9ca3af;
    line-height: 1.45;
    margin: 0;
}

/* Chat Message Styling */
[data-testid="stChatMessage"] {
    background: rgba(22, 27, 38, 0.75) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 18px !important;
    padding: 1.2rem 1.5rem !important;
    margin-bottom: 1.2rem !important;
    animation: slideUpFade 0.4s ease-out forwards;
    transition: all 0.3s ease;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(255, 215, 0, 0.3) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

/* Assistant Message Accent */
[data-testid="stChatMessage"][aria-label*="assistant"],
[data-testid="stChatMessage"]:nth-child(even) {
    background: rgba(26, 32, 48, 0.85) !important;
    border-left: 4px solid #FFD700 !important;
}

/* Sidebar Customization (unchanged structure, refined polish only) */
[data-testid="stSidebar"] {
    background-color: #0c0f17 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.sidebar-badge {
    background: rgba(255, 215, 0, 0.1);
    border: 1px solid rgba(255, 215, 0, 0.3);
    color: #FFD700;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 1rem;
}

/* Buttons Styling */
.stButton > button {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 165, 0, 0.1) 100%) !important;
    color: #FFD700 !important;
    border: 1px solid rgba(255, 215, 0, 0.4) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
    color: #0b0e14 !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4) !important;
    transform: translateY(-2px) !important;
}

/* Suggestion Pills */
.pill-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #d1d5db;
    margin-bottom: 0.6rem;
    text-align: center;
}

/* Chat Input Styling & Golden Glow Animation */
@keyframes borderGlowSweep {
    0% {
        border-color: rgba(255, 215, 0, 0.35);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2), inset 0 0 12px rgba(255, 215, 0, 0.05);
    }
    50% {
        border-color: rgba(255, 215, 0, 0.95);
        box-shadow: 0 0 32px rgba(255, 215, 0, 0.5), 0 0 50px rgba(255, 165, 0, 0.25), inset 0 0 20px rgba(255, 215, 0, 0.15);
    }
    100% {
        border-color: rgba(255, 215, 0, 0.35);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2), inset 0 0 12px rgba(255, 215, 0, 0.05);
    }
}

@keyframes sparkRotate {
    0% { transform: translateY(-50%) rotate(0deg) scale(1); filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.7)); }
    50% { transform: translateY(-50%) rotate(15deg) scale(1.2); filter: drop-shadow(0 0 18px rgba(255, 215, 0, 1)); }
    100% { transform: translateY(-50%) rotate(0deg) scale(1); filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.7)); }
}

[data-testid="stChatInput"] {
    position: relative !important;
    border-radius: 22px !important;
    border: 1.5px solid rgba(255, 215, 0, 0.5) !important;
    background: rgba(16, 20, 30, 0.94) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    padding: 0.35rem 0.5rem !important;
    animation: borderGlowSweep 3.5s ease-in-out infinite !important;
    transition: all 0.3s ease !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #FFD700 !important;
    box-shadow: 0 0 35px rgba(255, 215, 0, 0.65), inset 0 0 20px rgba(255, 215, 0, 0.2) !important;
}

[data-testid="stChatInput"] textarea {
    padding-left: 2.8rem !important;
    font-size: 0.98rem !important;
    color: #f3f4f6 !important;
    background: transparent !important;
}

[data-testid="stChatInput"]::before {
    content: "✨";
    position: absolute;
    left: 18px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.25rem;
    animation: sparkRotate 3s ease-in-out infinite;
    z-index: 10;
    pointer-events: none;
}

[data-testid="stChatInputSubmitButton"] {
    background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
    border-radius: 50% !important;
    border: none !important;
    width: 38px !important;
    height: 38px !important;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.45) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stChatInputSubmitButton"]:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.85) !important;
}

[data-testid="stChatInputSubmitButton"] svg {
    fill: #0b0e14 !important;
    color: #0b0e14 !important;
}

/* Status Indicator */
.model-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: #10B981;
    margin-top: 10px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background-color: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10B981;
    animation: pulseBorder 2.5s ease-in-out infinite;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. Environment & Model Initialization (Auto-Fallback)
# ---------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ **GEMINI_API_KEY not found!** Please set your API key in the `.env` file.")
    st.stop()

genai.configure(api_key=API_KEY)

@st.cache_resource
def get_working_model():
    """Dynamically detects and selects an active working Gemini model."""
    candidates = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-flash-latest",
        "gemini-3.1-flash-lite",
        "gemini-flash-lite-latest"
    ]
    for model_name in candidates:
        try:
            m = genai.GenerativeModel(model_name)
            res = m.generate_content("ping")
            if res and res.text:
                return m, model_name
        except Exception:
            continue
    # Safe default if all probes fail
    return genai.GenerativeModel("gemini-3.6-flash"), "gemini-3.6-flash"

try:
    model, active_model_name = get_working_model()
except Exception as e:
    st.error(f"❌ Failed to connect to Gemini API: {e}")
    st.stop()

# ---------------------------------------------------------
# 4. Session State Management
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# ---------------------------------------------------------
# 5. Sidebar Layout & Options
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='font-family: Cinzel; color: #FFD700; text-align: center; margin-bottom: 0; font-size: 1.8rem;'>🏛️ HISTORIC AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.75rem; letter-spacing: 1px; margin-bottom: 1.2rem; text-transform: uppercase;'>Discover the World's Heritage</p>", unsafe_allow_html=True)

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='model-status'>
        <div class='status-dot'></div>
        <span>Model: <b>{active_model_name}</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Persona Mode")
    response_mode = st.selectbox(
        "Choose AI Response Style:",
        ["📜 Comprehensive Guide", "⚡ Quick Summary", "🎭 Immersive Storyteller"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🛠️ Controls")

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col_nav2:
        if st.session_state.messages:
            chat_json = json.dumps(st.session_state.messages, indent=2)
            st.download_button(
                label="📥 Export",
                data=chat_json,
                file_name="historic_ai_chat.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.button("📥 Export", disabled=True, use_container_width=True)

    st.markdown("---")
    st.write(f"💬 **Total Queries:** {len(st.session_state.messages) // 2}")

    # User Profile Card at Sidebar Bottom
    st.markdown("""
    <div style="margin-top: 3rem; padding: 0.8rem 1rem; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 215, 0, 0.2); border-radius: 14px; display: flex; align-items: center; gap: 12px;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 165, 0, 0.1)); border: 1px solid rgba(255, 215, 0, 0.5); display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">🏛️</div>
        <div>
            <div style="font-weight: 700; font-size: 0.88rem; color: #f3f4f6;">Karthik Kalal</div>
            <div style="font-size: 0.72rem; color: #9ca3af;">Free Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Top Header Bar & Hero Banner
# ---------------------------------------------------------
# Top Bar matching UI mockup
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0.5rem 1.5rem 0.5rem;">
    <div style="background: rgba(255, 215, 0, 0.08); border: 1px solid rgba(255, 215, 0, 0.25); border-radius: 20px; padding: 6px 14px; font-size: 0.83rem; color: #FFD700; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;">
        <span>✨ {active_model_name}</span>
    </div>
    <div style="display: flex; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 6px 14px; font-size: 0.82rem; color: #d1d5db; font-weight: 500;">⚙️ Settings</div>
        <div style="background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 6px 14px; font-size: 0.82rem; color: #d1d5db; font-weight: 500;">📤 Export</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-container">
    <div class="hero-icon-wrap">
        <div class="hero-icon">🏛️</div>
    </div>
    <div class="hero-title">Welcome to Historic AI</div>
    <div class="hero-subtitle">Ask anything. Discover history. Explore civilizations.</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. Quick Suggestion Pills (shown only if no messages yet)
# ---------------------------------------------------------
if len(st.session_state.messages) == 0:
    st.markdown("<div class='pill-title'>✨ Explore a topic:</div>", unsafe_allow_html=True)
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1:
        if st.button("🏛️ Hampi", use_container_width=True):
            st.session_state.preset_prompt = "Tell me everything about the history of Hampi, Karnataka"
    with p2:
        if st.button("📐 Pyramids", use_container_width=True):
            st.session_state.preset_prompt = "Explore the Great Pyramids of Giza, Egypt"
    with p3:
        if st.button("⚔️ Colosseum", use_container_width=True):
            st.session_state.preset_prompt = "Tell me about the Roman Colosseum's history and battles"
    with p4:
        if st.button("🏯 Kyoto", use_container_width=True):
            st.session_state.preset_prompt = "Discover the ancient history and temples of Kyoto, Japan"
    with p5:
        if st.button("🗿 Machu Picchu", use_container_width=True):
            st.session_state.preset_prompt = "Explain the Inca history of Machu Picchu"


# ---------------------------------------------------------
# 8. Render Existing Chat Messages
# ---------------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🏛️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ---------------------------------------------------------
# 9. Handle Input & AI Generation
# ---------------------------------------------------------
user_input = st.chat_input("Ask anything about history...")

# Check if preset pill was clicked
if st.session_state.preset_prompt:
    query = st.session_state.preset_prompt
    st.session_state.preset_prompt = None
elif user_input:
    query = user_input
else:
    query = None

if query:
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(query)

    # Build Prompt based on Persona Mode & Chat Context
    mode_instructions = ""
    if response_mode == "⚡ Quick Summary":
        mode_instructions = "Format your answer as a concise executive summary with high-impact bullet points and key takeaways."
    elif response_mode == "🎭 Immersive Storyteller":
        mode_instructions = "Adopt an immersive first-person narrator tone like a time traveler bringing history vividly to life with rich descriptions and dramatic flair."
    else:
        mode_instructions = """
Format your response using structured, beautifully organized markdown sections:
# 📍 Overview
# 📜 Historical Background
# 👑 Kings / Rulers & Dynasties
# 🏛 Architectural Wonders
# ⚔ Major Historical Events & Battles
# 📅 Key Timeline
# 🌍 Cultural & Religious Significance
# ⭐ Mind-Blowing Historical Facts
# 🧭 Present-Day Status & Tourism Info
"""

    # Build prompt with conversation history context
    conversation_context = ""
    for past_msg in st.session_state.messages[-6:-1]:  # Keep last 5 messages for context
        role = "User" if past_msg["role"] == "user" else "Historic AI"
        conversation_context += f"{role}: {past_msg['content']}\n"

    system_prompt = f"""
You are Historic AI — a specialized AI historian, archivist, and cultural heritage expert dedicated EXCLUSIVELY to world history, ancient & medieval civilizations, historical figures, dynasties, monuments, archaeology, past battles, and cultural heritage.

User Question: "{query}"

{f'Recent Conversation History:\n{conversation_context}' if conversation_context else ''}

CRITICAL DOMAIN SCOPE RULE:
- BEFORE responding, determine if the user's prompt is related to history, historical events, ancient/medieval/modern historical figures, heritage sites, monuments, archaeology, past civilizations, or cultural heritage.
- IF THE QUESTION IS NOT RELATED TO HISTORY (e.g., programming/coding, mathematics, current tech news, modern daily weather, recipes, non-historical general advice, personal topics, science queries unrelated to historical origins):
  YOU MUST POLITELY DENY THE REQUEST.
  Specifically:
  1. Politely state that as Historic AI, your expertise is strictly limited to world history, ancient civilizations, monuments, and cultural heritage.
  2. Provide brief context explaining why the question falls outside historical archives/scope.
  3. Suggest 2-3 engaging historical topics or invite the user to ask any question about history, dynasties, or ancient marvels instead.

Instructions for Valid History Queries:
{mode_instructions}

Rules for Valid History Queries:
- Provide accurate, verified historical facts.
- Use clear, elegant markdown with emojis for high readability.
"""

    # Stream Assistant Response
    with st.chat_message("assistant", avatar="🏛️"):
        with st.status("🏛️ Researching historical archives...", expanded=True) as status:
            time.sleep(0.3)
            status.update(label="📜 Uncovering dynasties & architectural records...", state="running")
            time.sleep(0.3)
            status.update(label="✨ Synthesizing historical response...", state="complete", expanded=False)

        full_response = ""
        response_stream = None

        # Try generation with primary model, fallback to candidates if needed
        fallback_models = [active_model_name, "gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest", "gemini-3.1-flash-lite", "gemini-flash-lite-latest"]
        used_model = None

        for candidate_name in list(dict.fromkeys(fallback_models)):
            try:
                m = genai.GenerativeModel(candidate_name)
                response_stream = m.generate_content(system_prompt, stream=True)
                used_model = candidate_name
                break
            except Exception:
                continue

        if response_stream and used_model:
            try:
                def stream_chunks():
                    for chunk in response_stream:
                        try:
                            if chunk.text:
                                yield chunk.text
                        except Exception:
                            continue

                full_response = st.write_stream(stream_chunks)
            except Exception as err:
                full_response = f"⚠️ **Error generating response:** {err}\n\nPlease try again or click **New Chat**."
                st.error(full_response)
        else:
            full_response = "⚠️ **Unable to connect to Gemini models at the moment.** Please verify your API key or quota and try again."
            st.error(full_response)

    # Save Assistant Response to Session State
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Rerun if triggered via preset button to refresh UI state properly
    if user_input is None:
        st.rerun()