import requests
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ArcAssistAPI:
    def __init__(self, api_key, base_url="https://arc.rexter.co.uk/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, params=None, data=None, files=None, max_retries=3):
        """Handles API requests with retries, error handling, and debugging."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        for attempt in range(1, max_retries + 1):
            try:
                logging.debug(f"Attempt {attempt}: {method.upper()} {url}")
                if params:
                    logging.debug(f"Params: {params}")
                if data:
                    logging.debug(f"Data: {data}")

                response = requests.request(method, url, headers=self.headers, params=params, json=data, files=files)
                
                if response.status_code == 200:
                    logging.debug("Success! ✅")
                    try:
                        return response.json()  # Handle empty responses
                    except ValueError:
                        logging.error("Error: Empty or invalid JSON response.")
                        return None
                else:
                    logging.error(f"Request failed: {response.status_code} - {response.text}")

                if response.status_code in [500, 502, 503, 504]:
                    logging.debug("Retrying due to server error...")
                    time.sleep(2)
                    continue
                else:
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"Exception occurred: {e}")
                time.sleep(2)
        return None

    # ----------------------
    # Authentication
    # ----------------------
    def get_auth_status(self):
        return self._request("GET", "auth")
    
    # ----------------------
    # Admin Endpoints
    # ----------------------
    def is_multi_user_mode(self):
        return self._request("GET", "admin/is-multi-user-mode")
    
    def get_users(self):
        return self._request("GET", "admin/users")
    
    def create_user(self, user_data):
        return self._request("POST", "admin/users/new", data=user_data)
    
    def update_user(self, user_id, user_data):
        return self._request("POST", f"admin/users/{user_id}", data=user_data)
    
    def delete_user(self, user_id):
        return self._request("DELETE", f"admin/users/{user_id}")
    
    def get_admin_invites(self):
        return self._request("GET", "admin/invites")
    
    def create_admin_invite(self, invite_data):
        return self._request("POST", "admin/invite/new", data=invite_data)
    
    def delete_admin_invite(self, invite_id):
        return self._request("DELETE", f"admin/invite/{invite_id}")
    
    def get_admin_workspace_users(self, workspace_id):
        return self._request("GET", f"admin/workspaces/{workspace_id}/users")
    
    def update_admin_workspace_users(self, workspace_id, user_data):
        return self._request("POST", f"admin/workspaces/{workspace_id}/update-users", data=user_data)
    
    def manage_admin_workspace_users(self, workspace_slug, user_data):
        return self._request("POST", f"admin/workspaces/{workspace_slug}/manage-users", data=user_data)
    
    def admin_workspace_chats(self, chat_data):
        return self._request("POST", "admin/workspace-chats", data=chat_data)
    
    def update_admin_preferences(self, preference_data):
        return self._request("POST", "admin/preferences", data=preference_data)

    # ----------------------
    # Documents Endpoints
    # ----------------------
    def upload_document(self, file_path, folder_name=None):
        # If folder_name is provided, use the folder-specific endpoint.
        endpoint = f"document/upload/{folder_name}" if folder_name else "document/upload"
        with open(file_path, "rb") as file:
            files = {"file": file}
            return self._request("POST", endpoint, files=files)
    
    def upload_document_link(self, data):
        return self._request("POST", "document/upload-link", data=data)
    
    def upload_document_raw_text(self, data):
        return self._request("POST", "document/raw-text", data=data)
    
    def get_documents(self):
        return self._request("GET", "documents")
    
    def get_documents_in_folder(self, folder_name):
        return self._request("GET", f"documents/folder/{folder_name}")
    
    def get_document_accepted_file_types(self):
        return self._request("GET", "document/accepted-file-types")
    
    def get_document_metadata_schema(self):
        return self._request("GET", "document/metadata-schema")
    
    def get_document(self, doc_name):
        return self._request("GET", f"document/{doc_name}")
    
    def create_document_folder(self, data):
        return self._request("POST", "document/create-folder", data=data)
    
    def move_document_files(self, data):
        return self._request("POST", "document/move-files", data=data)

    # ----------------------
    # Workspaces Endpoints
    # ----------------------
    def create_workspace(self, workspace_data):
        return self._request("POST", "workspace/new", data=workspace_data)
    
    def get_workspaces(self):
        return self._request("GET", "workspaces")
    
    def get_workspace_details(self, slug):
        return self._request("GET", f"workspace/{slug}")
    
    def delete_workspace(self, slug):
        return self._request("DELETE", f"workspace/{slug}")
    
    def update_workspace(self, slug, data):
        return self._request("POST", f"workspace/{slug}/update", data=data)
    
    def get_workspace_chats(self, slug):
        return self._request("GET", f"workspace/{slug}/chats")
    
    def update_workspace_embeddings(self, slug, data):
        return self._request("POST", f"workspace/{slug}/update-embeddings", data=data)
    
    def update_workspace_pin(self, slug, data):
        return self._request("POST", f"workspace/{slug}/update-pin", data=data)
    
    def workspace_chat(self, slug, data):
        return self._request("POST", f"workspace/{slug}/chat", data=data)
    
    def workspace_stream_chat(self, slug, data):
        return self._request("POST", f"workspace/{slug}/stream-chat", data=data)
    
    def workspace_vector_search(self, slug, data):
        return self._request("POST", f"workspace/{slug}/vector-search", data=data)

    # ----------------------
    # System Settings Endpoints
    # ----------------------
    def get_system_env_dump(self):
        return self._request("GET", "system/env-dump")
    
    def get_system_status(self):
        return self._request("GET", "system")
    
    def get_system_vector_count(self):
        return self._request("GET", "system/vector-count")
    
    def update_system_env(self, env_data):
        return self._request("POST", "system/update-env", data=env_data)
    
    def export_system_chats(self):
        return self._request("GET", "system/export-chats")
    
    def remove_system_documents(self):
        return self._request("DELETE", "system/remove-documents")

    # ----------------------
    # Workspace Threads Endpoints
    # ----------------------
    def create_workspace_thread(self, slug, thread_data):
        return self._request("POST", f"workspace/{slug}/thread/new", data=thread_data)
    
    def update_workspace_thread(self, slug, thread_slug, data):
        return self._request("POST", f"workspace/{slug}/thread/{thread_slug}/update", data=data)
    
    def delete_workspace_thread(self, slug, thread_slug):
        return self._request("DELETE", f"workspace/{slug}/thread/{thread_slug}")
    
    def get_workspace_thread_chats(self, slug, thread_slug):
        return self._request("GET", f"workspace/{slug}/thread/{thread_slug}/chats")
    
    def workspace_thread_chat(self, slug, thread_slug, data):
        return self._request("POST", f"workspace/{slug}/thread/{thread_slug}/chat", data=data)
    
    def workspace_thread_stream_chat(self, slug, thread_slug, data):
        return self._request("POST", f"workspace/{slug}/thread/{thread_slug}/stream-chat", data=data)

    # ----------------------
    # User Management Endpoints
    # ----------------------
    def get_all_users(self):
        return self._request("GET", "users")
    
    def issue_auth_token(self, user_id):
        return self._request("GET", f"users/{user_id}/issue-auth-token")

    # ----------------------
    # OpenAI Compatible Endpoints
    # ----------------------
    def get_openai_models(self):
        return self._request("GET", "openai/models")
    
    def openai_chat_completions(self, data):
        return self._request("POST", "openai/chat/completions", data=data)
    
    def openai_embeddings(self, data):
        return self._request("POST", "openai/embeddings", data=data)
    
    def get_openai_vector_stores(self):
        return self._request("GET", "openai/vector_stores")

    # ----------------------
    # Embed Endpoints
    # ----------------------
    def get_embed(self):
        return self._request("GET", "embed")
    
    def get_embed_chats(self, embed_uuid):
        return self._request("GET", f"embed/{embed_uuid}/chats")
    
    def get_embed_session_chats(self, embed_uuid, session_uuid):
        return self._request("GET", f"embed/{embed_uuid}/chats/{session_uuid}")
    
    def create_embed(self, data):
        return self._request("POST", "embed/new", data=data)
    
    def update_embed(self, embed_uuid, data):
        return self._request("POST", f"embed/{embed_uuid}", data=data)
    
    def delete_embed(self, embed_uuid):
        return self._request("DELETE", f"embed/{embed_uuid}")









