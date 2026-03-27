import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

st.title("Mr.Bot")

# Sidebar for API Key
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if api_key:
    # Connect to the AI Brain
    llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.1-8b-instant")

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)

    # Handle User Input
    if prompt := st.chat_input("Say hello!"):
        # 1. Add your message to the history
        new_msg = HumanMessage(content=prompt)
        st.session_state.messages.append(new_msg)
        st.chat_message("user").write(prompt)
        
        # 2. Ask the AI (The fix is right here!)
        response = llm.invoke(st.session_state.messages)
        
        # 3. Add AI's answer to the history
        st.session_state.messages.append(response)
        st.chat_message("assistant").write(response.content)
else:
    st.info("Please enter your Groq API Key in the sidebar to start chatting!")
