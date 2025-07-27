import streamlit as st

def init_session():
    if 'chat' not in st.session_state:
        st.session_state.chat = []
    if 'slots' not in st.session_state:
        st.session_state.slots = {}
    if 'intent' not in st.session_state:
        st.session_state.intent = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
