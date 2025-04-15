import os
import sys
sys.path.append("..")
from src.api_anythingllm import ArcAssistAPI
import streamlit as st
import json


with st.spinner("Wait for it...", show_time=True):
    # api_key = st.secrets["api_key"]  # Assuming the API key is stored in Streamlit secrets
    api_key = os.environ.get("API_KEY")
    api_client = ArcAssistAPI(api_key)

    if api_key == 'API':
        st.error("Error: Please login to use the chatbot.")
        st.stop()


    def get_workspace_status():
        workspace_status = api_client.get_workspaces()
        if workspace_status is not None:
            workspace_status = api_client.get_workspaces()
            workspaces = [workspace["slug"] for workspace in workspace_status['workspaces']]
            page = st.sidebar.selectbox("Select a workspace:", workspaces, key = "workspace: <uniquevalueofsomesort>")
            # st.sidebar.write("Selected workspace:", page)
            return page
        else:
            return None


    def create_new_thread(page):
        # Create a new thread
        new_thread = api_client.create_workspace_thread(page, {"userId": 1})
        if new_thread:
            # fecth the thread slug from the response
            thread_slug = new_thread['thread']['slug']
            # Display the new thread slug
            return thread_slug            
        else:
            st.sidebar.error("Error: Unable to create a new thread.")
            return False

    def get_workspace_threads(page):
        workspace_threads = api_client.get_workspace_details(page)
        threads = [thread["threads"] for thread in workspace_threads['workspace']]
        slugs = [slug['slug'] for slug in threads[0]]
        thread_slug = st.sidebar.selectbox("Select a thread:", slugs, key = "thread: <uniquevalueofsomesort>")
        if st.sidebar.button("+ Add new thread", key = "add_thread: <uniquevalueofsomesort>"):
            thread_slug_new = create_new_thread(page)
            if thread_slug_new:
                st.sidebar.success("New thread created successfully.")
                thread_slug = thread_slug_new
                return thread_slug
            else:
                st.sidebar.error("Error: Unable to create a new thread.")
        return thread_slug


    def get_workspace_chats(page, thread_slug):
        workspace_chats = api_client.get_workspace_thread_chats(page, thread_slug)

        # Display the workspace chats in json format
        if workspace_chats:
            # Check if the workspace chats are empty
            if not workspace_chats['history']:
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.write("No chats found in this workspace.")
                    st.write("You can start new chats by sending a message.")

            # Display the workspace chats in chat format with st.info is role is user and st.success if role is assistant
            for chat in workspace_chats['history']:
                if chat['role'] == 'user':
                    ## Check if user sent an image
                    if chat['attachments']:
                        # Image types
                        image_types = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"]
                        # Check if the attachment is an image
                        if chat['attachments'][0]['mime'] in image_types:
                            caption = chat['attachments'][0]['name']
                            # Capture the image which is base64 encoded
                            image_data = chat['attachments'][0]['contentString']
                            # Display the image
                            # Display image on the right side on streamlit
                            col1, col2 = st.columns([2, 1])
                            with col2:
                                st.image(image_data, caption=caption, width=400)
                            # st.image(image_data, caption="User image", width=400)
                        st.info(chat['content'])
                    else:
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
        
    def load_chats(page):
        thread_slug = get_workspace_threads(page)

        if thread_slug:
            chat_start = get_workspace_chats(page, thread_slug)

        return thread_slug





    page = get_workspace_status()

    if page:
        thread_slug = load_chats(page)
        st.sidebar.button("Delete thread", key = "delete_thread: <uniquevalueofsomesort>", on_click=api_client.delete_workspace_thread, args=(page, thread_slug))

        user_input = st.chat_input(
            "Say something and/or attach an image",
            accept_file=True,
            file_type=["plet"],
            )

        if user_input:
            # st.write(type(user_input['text']))
            response = api_client.workspace_thread_chat(page, thread_slug, {"message": user_input['text'], "mode": "query", "attachments": []})
            if response:
                st.rerun()
            else:
                st.error("Error: Unable to get a response from the chatbot.")