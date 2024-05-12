from  ollama_api import ask_local
from groq_api import ask_groq

import streamlit as st
import time
import random



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversations = []
    st.session_state.conversation_count=1
    st.session_state.model_runtime = None
    st.session_state.selected_model_name= None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Runtime options
model_options = {
    "local": ["llama3","gemma:2b","gemma:7b","phi3","mistral","command-r","dbrx"],
    "Groq": ["gemma-7b-it","llama3-8b-8192", "llama3-70b-8192","mixtral-8x7b-32768"]
}

def conversation_click(messages:[]):
    print(f"Link Clicked {messages}")
    st.session_state.messages=messages

def ask(runtime:str,name:str,messages:[]) -> str :
    if runtime=="local":
        return ask_local(name, messages)
    elif runtime=="Groq": 
        return ask_groq(name, messages)

def newConversation():
    
    if prompt:= st.chat_input("How can i help ?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        ## Add Spinner 
        with st.spinner("Thinking..."):
            response= ask(st.session_state.model_runtime, st.session_state.selected_model_name, st.session_state.messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            print(response)
            model_reply = f"{st.session_state.model_runtime} ({st.session_state.selected_model_name}): {response}"
            st.markdown(model_reply)
            st.markdown(f"#### Reply from:  {st.session_state.model_runtime} ({st.session_state.selected_model_name}) ")
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        


def start_new_conversation():
    current_value = st.session_state.conversation_count

    ##clone st.session_state.messages
    old_message = []
    for m in st.session_state.messages:
        old_message.append(m)

    with st.spinner("Starting new..."):
        st.session_state.messages.append({"role": "user", "content": "Give me 1 line title for conversation. Not more than 50 words"})
        print("Asking for title....." + str(st.session_state.model_runtime))
        title= ask(st.session_state.model_runtime, st.session_state.selected_model_name, st.session_state.messages)
        print(f"Title is {title}")

        st.session_state.conversations.append({"name":f"{title}-{current_value}", "value":old_message})
        st.session_state.messages=[]
        st.session_state.conversation_count = current_value+1


if __name__ == "__main__":

    st.title(f"How can i help you today")
    with st.sidebar:
        st.title("Settings")
        new_action = st.button("New Conversation")
        if new_action:
            start_new_conversation()

        st.session_state.model_runtime = st.selectbox("Runtime", list(model_options.keys()), key="runtime_dropdown")
        
        if st.session_state.model_runtime:
            model_name_options = model_options[st.session_state.model_runtime]
            # Display the second dropdown with filtered options
            st.session_state.selected_model_name = st.selectbox("Model Name", model_name_options, key="model_dropdown")
        else:
            # Disable or display a placeholder for the second dropdown when runtime is not selected
            st.session_state.model_runtime=st.selectbox("Model Name", ["Please select a runtime first"], key="model_dropdown", disabled=True)

    
    expander = st.sidebar.expander("Conversations !", expanded=False)
    with expander:
      for conversation in st.session_state.conversations:
        st.button(conversation["name"],on_click=conversation_click, args=(conversation["value"],))
    

        #st.image("(link unavailable) Streamlit-logo.png")

    newConversation()

    