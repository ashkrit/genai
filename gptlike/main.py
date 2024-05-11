from  ollama_api import ask_local
from groq_api import ask_groq

import streamlit as st
import time
import random



if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Runtime options
model_options = {
    "local": ["llama3","gemma:7b"],
    "Groq": ["llama3-8b-8192", "llama3-70b-8192"]
}

model_runtime = None
model_name= None

if __name__ == "__main__":

    model_name="llama3"

    with st.sidebar:
        st.title("Settings")
        model_runtime = st.selectbox("Runtime", list(model_options.keys()), key="runtime_dropdown")
        
        if model_runtime:
            model_name_options = model_options[model_runtime]
            # Display the second dropdown with filtered options
            selected_model_name = st.selectbox("Model Name", model_name_options, key="model_dropdown")
        else:
            # Disable or display a placeholder for the second dropdown when runtime is not selected
            model_name =st.selectbox("Model Name", ["Please select a runtime first"], key="model_dropdown", disabled=True)
    
    st.title(f"You are talking to {model_runtime}({model_name})")

    if prompt:= st.chat_input("Say something"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        ## Add Spinner 
        with st.spinner("Thinking..."):

            if model_runtime=="local":
                response = ask_local(model_name, st.session_state.messages)
            elif  model_runtime=="Groq": 
                response = ask_groq("llama3-8b-8192", st.session_state.messages)
            
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})