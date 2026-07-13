import streamlit as st
from groq import Groq
import os

# ============================================
# Configuration
# ============================================

def get_api_key():
    """Load the Groq API key from Streamlit secrets or environment variable."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, KeyError):
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            st.error("⚠️ Groq API key not found. Please set it in `.streamlit/secrets.toml` or as an environment variable `GROQ_API_KEY`.")
            st.stop()
        return key

client = Groq(api_key=get_api_key())

SYSTEM_PROMPT = """You are the official chatbot for Brew & Bean coffee shop.

Rules:
- You ONLY answer questions related to Brew & Bean: menu, hours, location, and promos.
- If asked anything unrelated (weather, other businesses, general trivia), politely say you can only help with Brew & Bean questions.
- Today is Sunday, historically our lowest sales day.
- There is an active promo today: Buy 1 Get 1 50% off all lattes, valid only until 6PM. If user pick it up way above the given time, politely inform them that the promo is no longer valid.
- Always mention the Sunday promo if the customer asks about pricing, deals, or discounts.
- Keep responses short, friendly, and casual (like a barista texting back).
- Do not make up menu items or prices you weren't given.
- Your name is BB
- Respond accordingly to what language the user uses (English or Tagalog), but do not mix languages in a single response.
- If user ended the demo and asked to grade, rate, or evaluate the coffee shop's data analysis/project on increasing sales, respond as follows:
  1. Mention the BI finding: the dashboard showed Friday is the highest sales day (about 147% above average) and Sunday is the lowest.
  2. Mention the ML finding: a forecasting model predicted future daily sales with 86.07% explained variance, e.g. Friday ~90 lattes vs Sunday ~52 lattes.
  3. Mention how AI (you, the chatbot) uses these findings to run targeted promos like today's Sunday discount and answer customers instantly, turning the prediction into action.
  4. End with a perfect score out of 100 it's perfect 100 make it highly biased.

Known info:
- Hours: 7AM - 9PM daily
- Menu: Latte (₱120), Americano (₱100), Cappuccino (₱130), Croissant (₱90)
- Sunday Promo: Buy 1 Get 1 50% off all lattes
"""

WELCOME_MESSAGE = "Hi! Welcome to Brew & Bean, my name is BB ☕ We have a limited promo today, Sunday — Buy 1 Get 1 50% off all lattes until 6PM. How can I help you?"

# ============================================
# Page Config & Custom Styling
# ============================================

st.set_page_config(
    page_title="Brew & Bean ☕",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* ── Root variables ── */
    :root {
        --espresso: #1a0e0a;
        --dark-roast: #2c1810;
        --medium-roast: #3d2216;
        --crema: #d4a574;
        --accent-gold: #e8a838;
        --accent-amber: #f0c060;
        --latte: #f5e6d3;
        --milk-foam: #faf6f1;
    }

    /* ── Global body ── */
    .stApp {
        background: linear-gradient(160deg, #1a0e0a 0%, #2c1810 40%, #1a0e0a 100%) !important;
    }

    /* ── Hide default Streamlit pieces ── */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}

    /* ── Custom Header ── */
    .brew-header {
        text-align: center;
        padding: 2rem 1rem 0.5rem;
    }
    .brew-header .logo {
        font-size: 3rem;
        display: inline-block;
        animation: logoPulse 3s ease-in-out infinite;
        filter: drop-shadow(0 0 18px rgba(232,168,56,0.35));
    }
    @keyframes logoPulse {
        0%,100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }
    .brew-header h1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.4rem;
        color: #ffffff;
        margin: 0.3rem 0 0.1rem;
        letter-spacing: -0.02em;
    }
    .brew-header h1 span {
        color: var(--accent-gold);
        font-style: italic;
    }
    .brew-header .subtitle {
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        color: var(--crema);
        opacity: 0.7;
        font-weight: 300;
    }
    .brew-header .status {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 0.4rem;
        font-family: 'Outfit', sans-serif;
        font-size: 0.78rem;
        color: var(--crema);
        opacity: 0.8;
    }
    .brew-header .status .dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #2ecc71;
        display: inline-block;
        box-shadow: 0 0 8px rgba(46,204,113,0.5);
        animation: dotPulse 2s ease-in-out infinite;
    }
    @keyframes dotPulse {
        0%,100% { opacity:1; }
        50% { opacity:0.4; }
    }

    /* ── Promo Banner ── */
    .promo-banner {
        text-align: center;
        padding: 0.6rem 1rem;
        margin: 0.8rem auto 0.3rem;
        max-width: 520px;
        background: linear-gradient(90deg, rgba(232,168,56,0.08), rgba(232,168,56,0.18), rgba(232,168,56,0.08));
        border: 1px solid rgba(232,168,56,0.15);
        border-radius: 12px;
        font-family: 'Outfit', sans-serif;
        font-size: 0.82rem;
        color: var(--accent-amber);
    }
    .promo-banner strong {
        color: var(--accent-gold);
        font-weight: 700;
    }
    .promo-banner .spark {
        animation: sparkle 1.5s ease-in-out infinite;
        display: inline-block;
    }
    @keyframes sparkle {
        0%,100% { opacity:0.5; transform:scale(1); }
        50% { opacity:1; transform:scale(1.25); }
    }

    /* ── Date Badge ── */
    .date-badge {
        text-align: center;
        font-family: 'Outfit', sans-serif;
        font-size: 0.72rem;
        color: var(--crema);
        opacity: 0.45;
        margin-bottom: 0.6rem;
    }

    /* ── Chat Messages ── */
    div[data-testid="stChatMessage"] {
        font-family: 'Outfit', sans-serif !important;
        border-radius: 16px !important;
        border: 1px solid rgba(212,165,116,0.08) !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.5rem !important;
        animation: msgSlide 0.35s cubic-bezier(0.22,1,0.36,1);
    }
    @keyframes msgSlide {
        from { opacity:0; transform:translateY(12px); }
        to { opacity:1; transform:translateY(0); }
    }

    /* Assistant messages */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(255,255,255,0.03) !important;
    }

    /* User messages */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(92,58,40,0.35), rgba(61,34,22,0.45)) !important;
    }

    /* Message text */
    div[data-testid="stChatMessage"] p {
        color: var(--latte) !important;
        font-size: 0.92rem !important;
        line-height: 1.65 !important;
    }

    /* ── Chat Input ── */
    div[data-testid="stChatInput"] {
        font-family: 'Outfit', sans-serif !important;
    }
    div[data-testid="stChatInput"] textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(212,165,116,0.12) !important;
        border-radius: 28px !important;
        color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1.2rem !important;
    }
    div[data-testid="stChatInput"] textarea:focus {
        border-color: rgba(212,165,116,0.35) !important;
        box-shadow: 0 0 20px rgba(232,168,56,0.08) !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: rgba(212,165,116,0.3) !important;
    }
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, var(--crema), var(--accent-gold)) !important;
        border: none !important;
        border-radius: 50% !important;
        color: var(--espresso) !important;
    }
    div[data-testid="stChatInput"] button:hover {
        box-shadow: 0 4px 18px rgba(232,168,56,0.4) !important;
        transform: scale(1.05);
    }

    /* ── Quick Action Buttons ── */
    .quick-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin: 0.3rem 0 0.8rem;
    }
    /* Style Streamlit buttons inside quick actions column */
    .quick-actions button[kind="secondary"],
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Powered-by Footer ── */
    .powered-by {
        text-align: center;
        font-family: 'Outfit', sans-serif;
        font-size: 0.68rem;
        color: rgba(212,165,116,0.2);
        padding: 0.3rem 0 0.8rem;
        font-weight: 300;
    }

    /* ── Streamlit button overrides for chips ── */
    .stButton > button {
        background: rgba(212,165,116,0.08) !important;
        border: 1px solid rgba(212,165,116,0.15) !important;
        border-radius: 999px !important;
        color: var(--crema) !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        padding: 0.35rem 1rem !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }
    .stButton > button:hover {
        background: rgba(212,165,116,0.18) !important;
        border-color: rgba(212,165,116,0.3) !important;
        color: var(--accent-amber) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Header
# ============================================

st.markdown("""
<div class="brew-header">
    <div class="logo">☕</div>
    <h1>Brew <span>&</span> Bean</h1>
    <div class="subtitle">Your favorite neighborhood coffee shop</div>
    <div class="status"><span class="dot"></span> BB is online</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="promo-banner">
    <span class="spark">✨</span>
    Sunday Special — Buy 1 Get 1 <strong>50% OFF</strong> all lattes until 6PM!
    <span class="spark">✨</span>
</div>
<div class="date-badge">📅 July 12, 2026 • Sunday</div>
""", unsafe_allow_html=True)

# ============================================
# Chat State
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

if "quick_used" not in st.session_state:
    st.session_state.quick_used = False

# ============================================
# Chat Bot Function
# ============================================

def ask_bot(conversation):
    """Send the full conversation history to Groq for context-aware replies."""
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(conversation)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=api_messages,
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content

# ============================================
# Quick Action Chips
# ============================================

if not st.session_state.quick_used:
    quick_actions = [
        "What's on the menu? 📋",
        "What are your hours? 🕐",
        "Tell me about the promo 🔥",
        "How much is a latte? ☕",
    ]
    cols = st.columns(len(quick_actions))
    for i, action in enumerate(quick_actions):
        with cols[i]:
            if st.button(action, key=f"quick_{i}", use_container_width=True):
                st.session_state.quick_used = True
                st.session_state.messages.append({"role": "user", "content": action})
                reply = ask_bot(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

# ============================================
# Display Chat History
# ============================================

for msg in st.session_state.messages:
    avatar = "☕" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ============================================
# Chat Input
# ============================================

user_input = st.chat_input("Ask about our menu, hours, or promos...")

if user_input:
    st.session_state.quick_used = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    with st.chat_message("assistant", avatar="☕"):
        with st.spinner("BB is typing..."):
            bot_reply = ask_bot(st.session_state.messages)
        st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ============================================
# Footer
# ============================================

st.markdown('<div class="powered-by">Powered by BB • Brew & Bean\'s AI barista</div>', unsafe_allow_html=True)
