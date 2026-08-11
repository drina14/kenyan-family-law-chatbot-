import sys
from pathlib import Path

import streamlit as st

SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from chatbot import LegalChatbot


st.set_page_config(
    page_title="NyumbaLex | Kenyan Family Law AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_html(content):
    st.markdown(content, unsafe_allow_html=True)


render_html("""
<style>

/* Main application background */
.stApp {
background: linear-gradient(135deg, #193546 0%, #065B98 55%, #1B7FDC 100%);
color: white;
}

/* Blend Streamlit's native top header into the gradient instead of
   leaving it as a separate dark bar */
header[data-testid="stHeader"] {
background: transparent;
}
[data-testid="stToolbar"] { visibility: hidden; }
[data-testid="stDecoration"] { visibility: hidden; }

/* Blend Streamlit's native bottom chat container into the gradient too,
   instead of it appearing as a solid dark strip */
div[data-testid="stBottom"] {
background: transparent;
}
div[data-testid="stBottom"] > div {
background: transparent;
}
div[data-testid="stBottomBlockContainer"] {
background: transparent;
max-width: 900px;
padding-bottom: 2.2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
background: linear-gradient(180deg, #193546 0%, #0f2836 100%);
border-right: 1px solid rgba(255,255,255,0.12);
}
section[data-testid="stSidebar"] > div {
padding-top: 2rem;
}
.sidebar-title {
font-size: 26px;
font-weight: 700;
color: #ffffff;
margin-bottom: 2px;
}
.sidebar-tagline {
font-size: 13px;
letter-spacing: 3px;
font-weight: 600;
color: #0DB8D3;
margin-bottom: 30px;
}
.sidebar-divider {
height: 1px;
background: rgba(255,255,255,0.18);
margin: 22px 0;
}
.sidebar-section-label {
color: #9fc0d0;
font-size: 13px;
letter-spacing: 2px;
font-weight: 600;
margin-top: 10px;
margin-bottom: 10px;
}
.sidebar-empty {
color: #82aabd;
font-size: 14px;
}
.sidebar-disclaimer {
color: #9fc0d0;
font-size: 12px;
line-height: 1.6;
border-top: 1px solid rgba(255,255,255,0.12);
padding-top: 16px;
margin-top: 24px;
}

/* Remove default Streamlit padding */
.block-container {
padding-top: 2rem;
padding-bottom: 2rem;
max-width: 1100px;
}

/* Header */
.header {
text-align: center;
padding: 2rem 1rem 1rem 1rem;
}
.header-icon {
font-size: 3rem;
margin-bottom: 0.5rem;
}
.title {
font-size: 3rem;
font-weight: 700;
color: white;
margin-bottom: 0.3rem;
}
.subtitle {
font-size: 1.1rem;
color: #DCEAF2;
margin-bottom: 1.5rem;
}

/* Chat messages */
.user-message {
background: rgba(6, 91, 152, 0.85);
border: 1px solid rgba(255, 255, 255, 0.15);
border-radius: 16px;
padding: 1rem 1.2rem;
margin: 1rem 0;
}
.assistant-message {
background: rgba(25, 53, 70, 0.9);
border: 1px solid rgba(255, 255, 255, 0.12);
border-radius: 16px;
padding: 1.3rem;
margin: 1rem 0;
}
.message-label {
font-weight: 700;
margin-bottom: 0.5rem;
color: #0DB8D3;
}

/* Sources */
.sources {
background: rgba(25, 53, 70, 0.75);
border-left: 4px solid #0DB8D3;
border-radius: 8px;
padding: 1rem 1.2rem;
margin-top: 1rem;
}
.sources-title {
font-weight: 700;
color: white;
margin-bottom: 0.5rem;
}

/* Disclaimer */
.disclaimer {
text-align: center;
color: #DCEAF2;
font-size: 0.8rem;
margin-top: 2rem;
opacity: 0.85;
}

/* Floating chat input */
.stChatInputContainer {
padding-bottom: 0.5rem;
}
div[data-testid="stChatInput"] {
background: rgba(25, 53, 70, 0.85);
backdrop-filter: blur(14px);
-webkit-backdrop-filter: blur(14px);
border: 1px solid rgba(255,255,255,0.18);
border-radius: 22px;
box-shadow: 0 12px 34px rgba(0,0,0,0.4);
}
div[data-testid="stChatInput"] textarea {
color: white;
}

/* Buttons */
.stButton button {
background-color: #065B98;
color: white;
border: 1px solid #0DB8D3;
border-radius: 10px;
}
.stButton button:hover {
background-color: #1B7FDC;
color: white;
}

</style>
""")


with st.sidebar:

    render_html('<div style="font-size:44px;">⚖️</div><div class="sidebar-title">NyumbaLex</div><div class="sidebar-tagline">KENYAN FAMILY LAW</div>')

    render_html('<div class="sidebar-divider"></div>')

    if st.button("＋  New Chat"):
        st.session_state.messages = []
        st.rerun()

    render_html('<div class="sidebar-section-label">CONVERSATION HISTORY</div>')

    if not st.session_state.get("messages"):
        render_html('<div class="sidebar-empty">No recent chats yet.</div>')
    else:
        user_turns = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        for turn in user_turns[-10:][::-1]:
            preview = turn if len(turn) <= 40 else turn[:40] + "..."
            render_html(f'<div class="sidebar-empty">💬 {preview}</div>')

    render_html('<div class="sidebar-divider"></div>')

    render_html('<div class="sidebar-disclaimer">Information provided by NyumbaLex is for informational purposes only and does not replace professional legal advice.</div>')


render_html('<div class="header"><div class="header-icon">⚖️</div><div class="title">NyumbaLex</div><div class="subtitle">Kenyan Family Law AI Assistant</div></div>')


if "chatbot" not in st.session_state:
    with st.spinner("Loading legal assistant..."):
        st.session_state.chatbot = LegalChatbot()


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    if message["role"] == "user":
        render_html(f'<div class="user-message"><div class="message-label">You</div>{message["content"]}</div>')

    else:
        render_html(f'<div class="assistant-message"><div class="message-label">NyumbaLex</div>{message["content"]}</div>')

        if message.get("sources"):
            render_html('<div class="sources"><div class="sources-title">Sources</div>')

            for source in message["sources"]:
                document = source.get("document_name", "Unknown document")
                page = source.get("page_number", "Unknown")
                st.markdown(f"- **{document}** — Page {page}")

            render_html('</div>')


question = st.chat_input("Ask a legal question...")


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    render_html(f'<div class="user-message"><div class="message-label">You</div>{question}</div>')

    with st.spinner("Searching the legal documents..."):
        response = st.session_state.chatbot.ask(question)

    answer = response.get("answer", "I was unable to generate an answer.")
    sources = response.get("sources", [])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )

    render_html(f'<div class="assistant-message"><div class="message-label">NyumbaLex</div>{answer}</div>')

    if sources:
        render_html('<div class="sources"><div class="sources-title">Sources</div>')

        for source in sources:
            document = source.get("document_name", "Unknown document")
            page = source.get("page_number", "Unknown")
            st.markdown(f"- **{document}** — Page {page}")

        render_html('</div>')


render_html('<div class="disclaimer">NyumbaLex provides legal information based on its available Kenyan legal documents. It is not a substitute for professional legal advice.</div>')