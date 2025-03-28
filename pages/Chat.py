import sys
sys.path.append("..")
from src.api_anythingllm import ArcAssistAPI
import streamlit as st
import json


def clear_text():
    st.session_state["text"] = ""

# Initialize the API client
api_key = st.secrets["api_key"]  # Assuming the API key is stored in Streamlit secrets
api_client = ArcAssistAPI(api_key)

# Streamlit page title
st.title("Chatbot Interface")


# Display Workspace availability
workspace_status = api_client.get_workspaces()

# Display the workspace status in json format
st.write("Workspace status:")
if workspace_status:
    # st.json(workspace_status)
    # Select a workspace
    workspaces = [workspace["slug"] for workspace in workspace_status['workspaces']]
    page = st.sidebar.selectbox("Select a workspace:", workspaces, key = "<uniquevalueofsomesort>")
    st.write("Selected workspace:", page)
else:
    st.error("Error: Unable to get workspace status.")



# Display the workspace chats history
workspace_chats = api_client.get_workspace_chats(page)

# Display the workspace chats in json format
if workspace_chats:
    # Display the workspace chats in chat format with st.info is role is user and st.success if role is assistant
    for chat in workspace_chats['history']:
        if chat['role'] == 'user':
            st.info(chat['content'])
        elif chat['role'] == 'assistant':
            st.success(chat['content'])
        
    # Also display the workspace chats in json format minimized
    st.write("Workspace chats:")
    st.json(workspace_chats, expanded=False)
else:
    st.error("Error: Unable to get workspace chats.")


# User input for the chatbot
user_input = st.text_input("Ask :", key="user_input")


# Button to send the message
if st.button("Send", on_click=clear_text):
    if user_input:
        # Call the API to get a response from the chatbot
        response = api_client.workspace_chat(page, {"message": user_input, "mode": "query", "attachments": []})
        # response = api_client.openai_chat_completions({"messages": [{"role": "user", "content": user_input}]})
        
        # Display the chatbot's response
        if response:
            # reload the page
            print(response)
            st.rerun()
        else:
            st.error("Error: Unable to get a response from the chatbot.")
    else:
        st.warning("Please enter a message.")


def run_chatbot():
    import app
    app.main
    st.title("Welcome to the Chatbot Application")