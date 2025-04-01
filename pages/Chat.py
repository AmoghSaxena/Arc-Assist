import os
import sys
sys.path.append("..")
from src.api_anythingllm import ArcAssistAPI
import streamlit as st
import json

# my_bar = st.progress(0, text='Loading Chat...')
with st.spinner("Wait for it...", show_time=True):
    # api_key = st.secrets["api_key"]  # Assuming the API key is stored in Streamlit secrets
    api_key = os.environ.get("API_KEY")
    api_client = ArcAssistAPI(api_key)

    if api_key == 'API':
        st.error("Error: Please login to use the chatbot.")
        st.stop()
    st.title("Chatbot Testing")


    def get_workspace_status():
        workspace_status = api_client.get_workspaces()
        if workspace_status is not None:
            workspace_status = api_client.get_workspaces()
            workspaces = [workspace["slug"] for workspace in workspace_status['workspaces']]
            page = st.sidebar.selectbox("Select a workspace:", workspaces, key = "workspace: <uniquevalueofsomesort>")
            st.sidebar.write("Selected workspace:", page)
            return page
        else:
            return None


    # Display the workspace threads in json format


    def get_workspace_threads(page):
        workspace_threads = api_client.get_workspace_details(page)
        threads = [thread["threads"] for thread in workspace_threads['workspace']]
        slugs = [slug['slug'] for slug in threads[0]]
        thread_slug = st.sidebar.selectbox("Select a thread:", slugs, key = "thread: <uniquevalueofsomesort>")
        st.sidebar.write("Selected thread:", thread_slug)
        return thread_slug


    def get_workspace_chats(page, thread_slug):
        workspace_chats = api_client.get_workspace_thread_chats(page, thread_slug)

        # Display the workspace chats in json format
        if workspace_chats:
            # Display the workspace chats in chat format with st.info is role is user and st.success if role is assistant
            for chat in workspace_chats['history']:
                if chat['role'] == 'user':
                    st.info(chat['content'])
                elif chat['role'] == 'assistant':
                    st.success(chat['content'])
                
            # Also display the workspace chats in json format minimized
            # st.write("Workspace chats:")
            # st.json(workspace_chats['history'], expanded=False)
            return True
        else:
            st.error("Error: Unable to get workspace chats.")
            return False


    page = get_workspace_status()

    if page:
        thread_slug = get_workspace_threads(page)

        if thread_slug:
            chat_start = get_workspace_chats(page, thread_slug)

            if chat_start:
                user_input = st.chat_input(
                    "Say something and/or attach an image",
                    accept_file=True,
                    file_type=["plet"],
                    )
                # st.write("User input:", user_input)

                if user_input:
                    # st.write(type(user_input['text']))
                    response = api_client.workspace_thread_chat(page, thread_slug, {"message": user_input['text'], "mode": "query", "attachments": []})
                    if response:
                        st.rerun()
                    else:
                        st.error("Error: Unable to get a response from the chatbot.")