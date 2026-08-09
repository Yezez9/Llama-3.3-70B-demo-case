import streamlit as st
import os
import sys
import re
from datetime import datetime
from groq import Groq

# ============================================
# Groq API Client
# ============================================

def get_api_key():
    """Load the Groq API key from Streamlit secrets or environment variable."""
    try:
        key = st.secrets["GROQ_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key
    st.error("⚠️ Groq API key not found. Set it in `.streamlit/secrets.toml` or as env var `GROQ_API_KEY`.")
    st.stop()

client = Groq(api_key=get_api_key())

# ============================================
# Configuration — Dataset Definitions
# ============================================
# Each dataset maps a display label to a file path.
# To add/remove datasets, just edit this dictionary.

DATASETS = {
    "NBA":      "datasets/dataset_1.md",
    "F1":       "datasets/dataset_2.md",
    "FIFA":     "datasets/dataset_3.md",
    "Soccer":   "datasets/dataset_4.md",
    "Olympics": "datasets/dataset_5.md",
}

# Color assignments for each dataset label (used in tags and checkboxes)
DATASET_COLORS = {
    "NBA":      "#0000FF",
    "F1":       "#FF0000",
    "FIFA":     "#FF00C8",
    "Soccer":   "#00FF11",
    "Olympics": "#00C7FF"
}

# Auto-included when ALL 5 datasets above are checked
CROSS_DATASET_FILE = "datasets/cross_dataset_summary.md"

# ============================================
# Core Functions — This is the backend logic
# ============================================

def load_dataset(filepath):
    """Read a single dataset file and return its contents as a string.

    Args:
        filepath: Relative path to the .md file (e.g. 'datasets/dataset_1.md')

    Returns:
        The file contents as a string, or an error message if the file is missing.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"[Error: File '{filepath}' not found]"


def build_prompt(checked_datasets, user_question):
    """Assemble the full prompt that gets sent to the LLM.

    This is the key function for the demo — it shows exactly how
    toggling checkboxes changes what context the model sees.

    Args:
        checked_datasets: List of dataset label strings that are currently
                          checked (e.g. ["NBA", "FIFA"]).
        user_question:    The user's chat message.

    Returns:
        A single string containing the system instruction, concatenated
        dataset context blocks, and the user's question.
    """
    # --- 1. System instruction ---
    system_block = (
        "SYSTEM: You are Stadium AI, a sports data analysis assistant. Answer the user's question "
        "using ONLY the dataset context provided below. If the answer isn't in "
        "the provided context, say so clearly.\n\n"
        "FORMATTING RULES:\n"
        "- When comparing metrics, present them clearly with the metric name, value, and unit.\n"
        "- Use bold for key names and values.\n"
        "- Keep explanations concise but insightful.\n"
        "- When referencing data sources, mention which dataset(s) the data comes from."
    )

    # --- 2. Build context from checked datasets ---
    context_blocks = []
    for label in checked_datasets:
        filepath = DATASETS[label]
        content = load_dataset(filepath)
        context_blocks.append(f"--- {label} ---\n{content}")

    # Auto-include cross-dataset summary when ALL 5 datasets are selected
    if set(checked_datasets) == set(DATASETS.keys()):
        cross_content = load_dataset(CROSS_DATASET_FILE)
        context_blocks.append(f"--- Cross-Dataset Summary ---\n{cross_content}")

    context_section = "CONTEXT:\n" + "\n\n".join(context_blocks)

    # --- 3. User question ---
    question_section = f"USER QUESTION:\n{user_question}"

    # --- 4. Combine everything ---
    full_prompt = f"{system_block}\n\n{context_section}\n\n{question_section}"
    return full_prompt


def call_llm(prompt):
    """Send the assembled prompt to the LLM (Groq — Llama 3.3 70B) and return the response.

    This is the ONE function you'd change to swap providers
    (OpenAI, Anthropic, Gemini, etc.). Nothing else in the app needs to change.

    Args:
        prompt: The fully assembled prompt string from build_prompt().

    Returns:
        The LLM's response as a string.
    """
    # Print full prompt to terminal for demo verification
    # (Uses sys.stdout.buffer to avoid Windows encoding errors with special characters)
    output = (
        "\n" + "=" * 60 + "\n"
        "FULL PROMPT SENT TO LLM:\n"
        + "=" * 60 + "\n"
        + prompt + "\n"
        + "=" * 60 + "\n"
    )
    try:
        sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
        sys.stdout.buffer.flush()
    except Exception:
        print(output.encode("ascii", errors="replace").decode("ascii"))

    # --- Real Groq API call using Llama 3.3 70B ---
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


# ============================================
# Page Config
# ============================================

st.set_page_config(
    page_title="Stadium AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Custom CSS — Complete UI Overhaul
# ============================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #0a0a0a !important;
    color: #e0e0e0 !important;
}

/* ── Hide Streamlit defaults ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d0d 0%, #111111 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
    padding: 0 !important;
    transform: none !important;
    position: relative !important;
}

/* Hide sidebar collapse/expand button */
button[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
button[kind="headerNoPadding"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

section[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem !important;
}

/* ── Main Content Area ── */
.main .block-container {
    max-width: 900px !important;
    padding: 1rem 2rem 6rem 2rem !important;
    margin: 0 auto !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ── Chat Input ── */
[data-testid="stChatInput"] {
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    background: #0a0a0a !important;
}

[data-testid="stChatInput"] textarea {
    background: #141414 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: #e0e0e0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.8rem 1.2rem !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #00c853 !important;
    box-shadow: 0 0 0 1px rgba(0,200,83,0.2) !important;
}

[data-testid="stChatInput"] button {
    background: #00c853 !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    border: none !important;
    color: #000 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] button:hover {
    background: #00e676 !important;
    transform: scale(1.05);
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.6rem 0 !important;
    gap: 0.8rem !important;
}

/* User message avatar */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageAvatarContainer"] {
    background: linear-gradient(135deg, #1a1a2e, #16213e) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
}

/* User message bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, #1a3a2a, #0f2d1f) !important;
    border: 1px solid rgba(0,200,83,0.15) !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 0.9rem 1.3rem !important;
    max-width: 75% !important;
    margin-left: auto !important;
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
}

/* Assistant message avatar */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageAvatarContainer"] {
    background: linear-gradient(135deg, #00c853, #00a844) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
}

/* Assistant message content */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
    background: #141414 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 1.2rem 1.4rem !important;
    max-width: 85% !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
}

/* ── Sidebar Checkboxes — Color-coded ── */
section[data-testid="stSidebar"] [data-testid="stCheckbox"] {
    padding: 0.15rem 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stCheckbox"] label {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
}

section[data-testid="stSidebar"] [data-testid="stCheckbox"] label p {
    font-size: 0.85rem !important;
}

/* ── Expander styling (for sidebar) ── */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}

/* ── Markdown inside chat ── */
[data-testid="stChatMessageContent"] p {
    margin-bottom: 0.5rem !important;
}

[data-testid="stChatMessageContent"] strong {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── Captions (dataset context tags) ── */
[data-testid="stChatMessageContent"] [data-testid="stCaption"] {
    font-size: 0.75rem !important;
    color: rgba(255,255,255,0.4) !important;
    margin-top: 0.6rem !important;
    padding-top: 0.6rem !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── Warning messages ── */
[data-testid="stAlert"] {
    background: rgba(255,152,0,0.08) !important;
    border: 1px solid rgba(255,152,0,0.2) !important;
    border-radius: 12px !important;
    color: #ffb74d !important;
}

/* ── Sidebar title override ── */
section[data-testid="stSidebar"] [data-testid="stMarkdown"] h4 {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.35) !important;
    margin-top: 1.8rem !important;
    margin-bottom: 0.6rem !important;
}

/* ── Dividers ── */
hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 0.8rem 0 !important;
}

/* ── Links ── */
a {
    color: #00c853 !important;
    text-decoration: none !important;
}
a:hover {
    color: #00e676 !important;
    text-decoration: underline !important;
}

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

[data-testid="stChatMessage"] {
    animation: fadeInUp 0.35s ease-out !important;
}

/* ── Custom HTML blocks ── */
.stadium-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.2rem 0 0.8rem 0;
}
.stadium-brand-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #00c853, #00a844);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.stadium-brand-text {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 0.08em;
    color: #ffffff;
}
.chat-nav-btn {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.55rem 0.9rem;
    margin: 0.3rem 0 0.5rem 0;
    cursor: default;
    transition: background 0.2s ease;
}
.chat-nav-btn:hover {
    background: rgba(255,255,255,0.07);
}
.chat-nav-icon {
    font-size: 1rem;
    opacity: 0.7;
}
.chat-nav-label {
    font-size: 0.88rem;
    font-weight: 500;
    color: #e0e0e0;
}

/* ── Timestamp ── */
.timestamp-header {
    text-align: center;
    padding: 1rem 0 0.6rem 0;
}
.timestamp-pill {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.72rem;
    font-weight: 500;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.03em;
}

/* ── Data source tag ── */
.data-source-tag {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ── Feedback row ── */
.feedback-row {
    display: flex;
    gap: 1.2rem;
    margin-top: 0.9rem;
    padding-top: 0.7rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.feedback-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.78rem;
    font-weight: 500;
    color: rgba(255,255,255,0.4);
    cursor: pointer;
    transition: color 0.2s ease;
    text-decoration: none !important;
    background: none;
    border: none;
    padding: 0;
}
.feedback-btn:hover {
    color: rgba(255,255,255,0.7) !important;
}

/* ── Query scope pills ── */
.query-scope {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0;
    flex-wrap: wrap;
}
.query-scope-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-right: 0.2rem;
}
.scope-pill {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.scope-pill-plus {
    font-weight: 700;
    opacity: 0.8;
}

/* ── Disclaimer ── */
.disclaimer {
    text-align: center;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.2);
    padding: 0.5rem 0 0.2rem 0;
}

/* ── Title override (hide default) ── */
h1 {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================
# Session State Initialization
# ============================================

# Chat history — each entry stores the message AND which datasets were active
if "messages" not in st.session_state:
    st.session_state.messages = []

# Checkbox states — default all unchecked
if "dataset_checks" not in st.session_state:
    st.session_state.dataset_checks = {label: False for label in DATASETS}

# Select-all toggle tracker
if "select_all" not in st.session_state:
    st.session_state.select_all = False

# ============================================
# Sidebar — Branding + Dataset Checkboxes
# ============================================

with st.sidebar:
    # Brand logo
    st.markdown("""
    <div class="stadium-brand">
        <div class="stadium-brand-icon">AI</div>
        <div class="stadium-brand-text">STADIUM</div>
    </div>
    """, unsafe_allow_html=True)

    # Chat nav button
    st.markdown("""
    <div class="chat-nav-btn">
        <span class="chat-nav-icon">💬</span>
        <span class="chat-nav-label">Chat</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### DATASET CONTEXT")

    # --- Callbacks for checkbox sync ---
    def on_select_all_change():
        """When Select All is toggled, sync every individual checkbox."""
        new_val = st.session_state.select_all_cb
        st.session_state.select_all = new_val
        for label in DATASETS:
            st.session_state.dataset_checks[label] = new_val
            st.session_state[f"cb_{label}"] = new_val

    def on_individual_change(label):
        """When any individual checkbox changes, update tracking and sync Select All."""
        st.session_state.dataset_checks[label] = st.session_state[f"cb_{label}"]
        all_checked = all(st.session_state.dataset_checks.values())
        st.session_state.select_all = all_checked
        st.session_state.select_all_cb = all_checked

    # --- Select All checkbox ---
    st.checkbox(
        "Select all",
        value=st.session_state.select_all,
        key="select_all_cb",
        on_change=on_select_all_change,
    )

    # --- Individual dataset checkboxes ---
    for label in DATASETS:
        color = DATASET_COLORS.get(label, "#78909c")
        st.checkbox(
            label,
            value=st.session_state.dataset_checks[label],
            key=f"cb_{label}",
            on_change=on_individual_change,
            args=(label,),
        )


# ============================================
# Helpers — Rich HTML rendering
# ============================================

def get_active_datasets():
    """Return list of currently checked dataset labels."""
    return [
        label for label, is_checked in st.session_state.dataset_checks.items()
        if is_checked
    ]

def render_data_source_tag(datasets):
    """Render a colored DATA SOURCE tag line."""
    if not datasets:
        return ""
    sources = " + ".join([f"{d} Data" for d in datasets])
    return f'<div class="data-source-tag" style="color: #00c853;">DATA SOURCE: {sources}</div>'

def render_feedback_row():
    """Render the Helpful / Report Issue feedback buttons."""
    return """
    <div class="feedback-row">
        <span class="feedback-btn">MADE BY GROUP 5</span>
        <span class="feedback-btn">LANCE, MARC, HASNEL, RALPH, DARDY</span>
    </div>
    """

def render_query_scope_pills(datasets):
    """Render the QUERY SCOPE pills above the input."""
    if not datasets:
        return ""
    pills_html = ""
    for d in datasets:
        color = DATASET_COLORS.get(d, "#78909c")
        pills_html += f'<span class="scope-pill" style="background: {color}22; color: {color};"><span class="scope-pill-plus">+</span>{d.upper()}</span>'
    return f"""
    <div class="query-scope">
        <span class="query-scope-label">QUERY SCOPE:</span>
        {pills_html}
    </div>
    """


# ============================================
# Main Chat Area
# ============================================

# Hidden title for Streamlit (we use our own branding)
st.title("Stadium AI")

# ============================================
# Timestamp header
# ============================================

now = datetime.now()
time_str = now.strftime("Today, %H:%M")
st.markdown(f"""
<div class="timestamp-header">
    <span class="timestamp-pill">{time_str}</span>
</div>
""", unsafe_allow_html=True)

# ============================================
# Display Chat History
# ============================================

for entry in st.session_state.messages:
    role = entry["role"]
    content = entry["content"]
    active_datasets = entry.get("active_datasets", [])

    with st.chat_message(role):
        if role == "assistant":
            # Rich response card with data source tag, content, and feedback
            source_tag = render_data_source_tag(active_datasets)
            feedback = render_feedback_row()
            st.markdown(source_tag, unsafe_allow_html=True)
            st.markdown(content)
            st.markdown(feedback, unsafe_allow_html=True)
        else:
            st.markdown(content)

# ============================================
# Query Scope + Chat Input + Disclaimer
# ============================================

checked = get_active_datasets()

# Show query scope pills
scope_html = render_query_scope_pills(checked)
if scope_html:
    st.markdown(scope_html, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask about player stats, team performance, or cross-dataset comparisons...")

# Disclaimer footer
st.markdown('<div class="disclaimer">Stadium AI can make mistakes. Verify critical stats. MADE BY GROUP 5</div>', unsafe_allow_html=True)

# ============================================
# Chat Input Processing
# ============================================

if user_input:
    # Store the user message (with dataset snapshot)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "active_datasets": checked,
    })

    # Guard: no datasets selected
    if len(checked) == 0:
        st.warning("⚠️ Select at least one dataset to chat.")
        # Still store a system note so the conversation doesn't look broken
        st.session_state.messages.append({
            "role": "assistant",
            "content": "⚠️ No datasets selected. Please check at least one dataset in the sidebar, then try again.",
            "active_datasets": [],
        })
        st.rerun()

    # Build prompt and call LLM
    prompt = build_prompt(checked, user_input)
    response = call_llm(prompt)

    # Store the assistant response (with dataset snapshot)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "active_datasets": checked,
    })

    st.rerun()
