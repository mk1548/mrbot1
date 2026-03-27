import streamlit as st
from langchain_groq import ChatGroq

# 1. Title of your webpage
st.title("🤖 My First Free Chatbot")

# 2. Use your API Key (We will put this in a secret spot later)
# For now, we use a placeholder
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if api_key:
    # 3. Connect to the AI Brain
    llm = ChatGroq(groq_api_key=api_key, model_name="llama3-8b-8192")

    # 4. Create the Chat Window
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Say hello!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # This line sends your text to the AI and gets an answer
        response = llm.invoke(st.session_state.messages)
        
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        st.chat_message("assistant").write(response.content)
else:
    st.info("Please enter your Groq API Key in the sidebar to start chatting!")
