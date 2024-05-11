from  ollama_api import ask_local
from groq_api import ask_groq

import streamlit as st
import time
import random

st.title("Gpt Style Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if __name__ == "__main__":

    model_name="llama3"

    if prompt:= st.chat_input("Say something"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        ## Add Spinner 
        with st.spinner("Thinking..."):
            #response = ask_local("llama3", st.session_state.messages)
            #response = ask_groq("llama3-8b-8192", st.session_state.messages)
            response = ask_groq("llama3-70b-8192", st.session_state.messages)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})