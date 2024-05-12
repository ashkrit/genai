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
    "local": ["llama3","gemma:2b","gemma:7b","phi3","mistral","command-r","dbrx"],
    "Groq": ["gemma-7b-it","llama3-8b-8192", "llama3-70b-8192","mixtral-8x7b-32768"]
}

model_runtime = None
selected_model_name= None


def newConversation():
    if prompt:= st.chat_input("How can i help ?"):
        st.title(f"You are talking to {model_runtime} ({selected_model_name})")
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        ## Add Spinner 
        with st.spinner("Thinking..."):

            if model_runtime=="local":
                response = ask_local(selected_model_name, st.session_state.messages)
            elif  model_runtime=="Groq": 
                response = ask_groq(selected_model_name, st.session_state.messages)
            
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            print(response)
            model_reply = f"{model_runtime} ({selected_model_name}): {response}"
            st.markdown(model_reply)
            st.markdown(f"#### Reply from:  {model_runtime} ({selected_model_name}) ")
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":

    with st.sidebar:
        st.title("Settings")
        model_runtime = st.selectbox("Runtime", list(model_options.keys()), key="runtime_dropdown")
        
        if model_runtime:
            model_name_options = model_options[model_runtime]
            # Display the second dropdown with filtered options
            selected_model_name = st.selectbox("Model Name", model_name_options, key="model_dropdown")
        else:
            # Disable or display a placeholder for the second dropdown when runtime is not selected
            model_runtime=st.selectbox("Model Name", ["Please select a runtime first"], key="model_dropdown", disabled=True)

    
    expander = st.sidebar.expander("Conversations !", expanded=False)

    with expander:
        new_action = st.button("New!")

        if new_action:
            st.session_state.messages=[]
            #st.stop()
            

        #st.image("(link unavailable) Streamlit-logo.png")
   
    newConversation()

    