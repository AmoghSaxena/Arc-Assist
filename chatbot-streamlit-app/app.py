import streamlit as st
from pages import Chat

def main():
    st.set_page_config(page_title="Chatbot App", layout="wide")
    
    st.title("Welcome to the Chatbot Application")
    st.sidebar.title("Navigation")
    
    page = st.sidebar.selectbox("Select a page:", ["Chatbot"])
    
    if page == "Chatbot":
        Chat.run_chatbot()

if __name__ == "__main__":
    main()