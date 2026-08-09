import streamlit as st
import os
import sys
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
        "SYSTEM: You are a data analysis assistant. Answer the user's question "
        "using ONLY the dataset context provided below. If the answer isn't in "
        "the provided context, say so clearly."
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
    page_icon="🏟️",
    layout="centered",
    initial_sidebar_state="expanded",
)

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
# Sidebar — Dataset Checkboxes
# ============================================

with st.sidebar:
    st.markdown("#### DATASET CONTEXT")

    # --- Select All checkbox ---
    select_all = st.checkbox("Select all", value=st.session_state.select_all)

    # If select-all was just toggled, sync all individual checkboxes
    if select_all != st.session_state.select_all:
        st.session_state.select_all = select_all
        for label in DATASETS:
            st.session_state.dataset_checks[label] = select_all
        st.rerun()

    # --- Individual dataset checkboxes ---
    for label in DATASETS:
        checked = st.checkbox(
            label,
            value=st.session_state.dataset_checks[label],
            key=f"cb_{label}",
        )
        st.session_state.dataset_checks[label] = checked

    # Keep select-all in sync: if user manually checks/unchecks individual boxes
    all_checked = all(st.session_state.dataset_checks.values())
    if st.session_state.select_all != all_checked:
        st.session_state.select_all = all_checked

# ============================================
# Main Chat Area — Header
# ============================================

st.title("🏟️ Stadium AI")

# ============================================
# Display Chat History
# ============================================

for entry in st.session_state.messages:
    role = entry["role"]
    content = entry["content"]
    active_datasets = entry.get("active_datasets", [])

    with st.chat_message(role):
        st.markdown(content)

        # Show which datasets were active for this message pair
        if role == "assistant" and active_datasets:
            dataset_tags = ", ".join(active_datasets)
            st.caption(f"📊 Context: {dataset_tags}")
        elif role == "assistant" and not active_datasets:
            st.caption("📊 Context: None")

# ============================================
# Chat Input & Processing
# ============================================

user_input = st.chat_input("Ask about player stats, team performance, or cross-dataset comparisons...")

if user_input:
    # Figure out which datasets are currently checked
    checked = [
        label for label, is_checked in st.session_state.dataset_checks.items()
        if is_checked
    ]

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
