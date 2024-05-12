from ollama_api import ask_local
from groq_api import ask_groq
from application_config import Config
import streamlit as st
import time
import random
import uuid
import json
import os
import datetime



app_config = Config("./app_config.json")
conversation_store=app_config.get("conversation.path")

## read file from given folders
def load_conversation(root_folder:str):
    for file_name in os.listdir(root_folder):
        if file_name.endswith(".json"):
            with open(os.path.join(root_folder, file_name), "r") as f:
                conversation = json.load(f)
                st.session_state.conversations.insert(0,conversation)



if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversations = []
    st.session_state.model_runtime = None
    st.session_state.selected_model_name= None
    load_conversation(conversation_store)

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

    ##clone st.session_state.messages
    old_message = []
    for m in st.session_state.messages:
        old_message.append(m)

    with st.spinner("Starting new..."):
        st.session_state.messages.append({"role": "user", "content": "Generate title for conversation so fat. It must be under 50 words"})
        print("Asking for title....." + str(st.session_state.model_runtime))
        title= ask(st.session_state.model_runtime, st.session_state.selected_model_name, st.session_state.messages)
        print(f"Title is {title}")

        conversation_record = {"name":f"{title}", 
                               "runtime":st.session_state.model_runtime,
                               "model": st.session_state.selected_model_name,
                               "value":old_message, 
                               "when":time.time()}
        message_id=str(uuid.uuid4())
        ## Get current time stamp as long 
    
        ## Write JSON to file 
        with open(f"{conversation_store}/{message_id}.json", "a") as f:
            json_text=json.dumps(conversation_record)
            f.write(f"{json_text}")

        st.session_state.conversations.insert(0,conversation_record)
        st.session_state.messages=[]
       


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

    
    expander = st.sidebar.expander("Conversations", expanded=True)
    with expander:
      for conversation in st.session_state.conversations:
        when = conversation["when"]
        e = datetime.datetime.fromtimestamp(when)
        user_friendly_time = e.strftime("%Y-%m-%d %H:%M:%S")
        tag = f"{user_friendly_time} - {conversation["name"]}"
        st.button(tag,on_click=conversation_click, args=(conversation["value"],))
    

        #st.image("(link unavailable) Streamlit-logo.png")

    newConversation()

    