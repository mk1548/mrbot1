import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. PAGE CONFIG (The Browser Tab Look) ---
st.set_page_config(page_title="Mr.Bot(Prototype1)", page_icon="🤖", layout="centered")

# --- 2. THE HEADER & LOGO ---
# You can replace the emoji with a URL to a hosted image/logo
st.markdown("<h1 style='text-align: center;'>Mr.Bot(Prototype1)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Powered by Llama 3.1, Idea by Mahant K.</p>", unsafe_allow_html=True)
st.divider()

# --- 3. THE SECRET KEY LOGIC ---
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Setup required: Add GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")

# --- 4. CHAT HISTORY & CLEAR BUTTON ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Floating 'Clear Chat' button in the sidebar
if st.sidebar.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.rerun()

# --- 5. DISPLAY MESSAGES WITH CUSTOM AVATARS ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg.content)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg.content)

# --- 6. USER INPUT ---
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.spinner("Thinking..."): # Added a loading spinner for better UX
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(response)
        
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.content)
