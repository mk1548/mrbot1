import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

st.title("🤖 My Public AI Bot")

# 1. Access the secret key (This looks for a hidden variable you'll set in Step 2)
# We use a try/except so the app doesn't crash if the key is missing
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please set it in Streamlit Cloud settings.")
    st.stop()

# 2. Setup the AI with the hidden key
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")

# 3. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    st.chat_message(role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)
    
    response = llm.invoke(st.session_state.messages)
    st.session_state.messages.append(response)
    st.chat_message("assistant").write(response.content)
