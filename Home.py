import streamlit as st

def main():
    # Set up the page configuration for the Streamlit app
    st.set_page_config(
        page_title='Groq Chatbot',   # Set the title of the web app
        page_icon='🤖',              # Add a robot emoji as the page icon
        layout='wide',               # Use a wide layout for more space
        initial_sidebar_state='expanded'  # Keep the sidebar expanded initially
    )
    
    st.title("Welcome to the Chatbot Application")
    st.sidebar.title("Navigation")
    
    # page = st.sidebar.selectbox("Select a page:", ["Chatbot"])
    pages = {
        "Chating Agent": [
            st.Page("pages/Chat.py", title="Anything LLM"),
            st.Page("pages/Groq.py", title="Groq Chat"),
        ],
        "Resources": [
            st.Page("pages/Login_Logout.py", title="Login and Logout"),
        ],
    }

    pg = st.navigation(pages)
    pg.run()
    
    # if page == "Chatbot":
    #     Chat.run()

if __name__ == "__main__":
    main()