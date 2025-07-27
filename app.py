import streamlit as st
from dialog_manager import handle_user_input
from context_manager import init_session
from rag_engine import get_rag_answer

# Page config
st.set_page_config(page_title="SmartBank Conversational AI", page_icon="💳", layout="wide")

# Inject terminal-style black theme and hide Streamlit default UI
st.markdown(
    """
    <style>
    html, body, #root, .main {
        height: 100%;
        margin: 0;
        background-color: #000000;
        color: #33ff33;
        font-family: monospace;
    }
    header, footer, .css-1d391kg > div:first-child {
        visibility: hidden;
        height: 0;
        width: 0;
        padding: 0;
        margin: 0;
    }
    .stTitle {
        color: #33ff33 !important;
        font-family: monospace !important;
        font-size: 40px !important;
        font-weight: bold !important;
        padding-top: 10px;
        padding-bottom: 20px;
        text-align: center;
    }
    .chat-bubble-user {
        text-align: right;
        background-color: #004d00;
        color: #a6f3a6;
        padding: 12px;
        border-radius: 15px;
        margin: 8px;
        font-family: monospace;
        font-size: 16px;
        max-width: 70%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .chat-bubble-bot {
        text-align: left;
        background-color: #000000;
        color: #33ff33;
        padding: 12px;
        border-radius: 15px;
        margin: 8px;
        font-family: monospace;
        font-size: 16px;
        max-width: 70%;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    div.stTextInput > label {
        color: #33ff33 !important;
        font-family: monospace;
    }
    input[type="text"] {
        background-color: #111111;
        color: #33ff33;
        border: 1px solid #33ff33;
        font-family: monospace;
    }
    button[kind="primary"] {
        background-color: #004d00 !important;
        color: #a6f3a6 !important;
        font-family: monospace !important;
        border-radius: 10px !important;
    }
    .css-18e3th9 {
        scrollbar-width: thin;
        scrollbar-color: #33ff33 #000000;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session vars
init_session()

def format_bot_message(msg):
    if not isinstance(msg, str):
        return "" if msg is None else str(msg)
    return msg.replace('\n', '<br>')

st.set_page_config(page_title="Smart Banking AI", page_icon="💳", layout="wide")

# Show welcome message on first run
if not st.session_state.chat:
    st.session_state.chat.append(("Bot", "Please enter your customer ID to continue."))

# Title section
st.markdown('<h1 class="stTitle">SmartBank Conversational AI</h1>', unsafe_allow_html=True)

# Show chat history
for speaker, msg in st.session_state.chat:
    if speaker == "You":
        st.markdown(f'<div class="chat-bubble-user">{msg}</div>', unsafe_allow_html=True)
    else:
        # For bot messages, use format_bot_message to preserve line breaks
        formatted_msg = format_bot_message(msg)
        st.markdown(f'<div class="chat-bubble-bot">{formatted_msg}</div>', unsafe_allow_html=True)

# User input box
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input(
        "You:", placeholder="Type your message...", label_visibility="collapsed", key="input_text"
    )
    submitted = st.form_submit_button("Send")

# Handle input
if submitted and user_input:
    st.session_state.chat.append(("You", user_input))
    response = handle_user_input(user_input)
    st.session_state.chat.append(("Bot", response))
    st.rerun()

    if st.button("Go"):
        if choice == "Logout":
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.intent = None
            st.session_state.slots = {}
            st.session_state.chat.append(("Bot", "You have been logged out. Please enter your customer ID to login again."))
        else:
            st.session_state.chat.append(("You", choice))
            response = handle_user_input(choice)
            st.session_state.chat.append(("Bot", response))
        
        # Hide menu after selection
        st.session_state.show_menu = False
        st.rerun()
