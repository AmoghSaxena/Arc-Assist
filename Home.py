# Import necessary modules
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import random
from datetime import datetime
from api_anythingllm import ArcAssistAPI

# Placeholder for the API key - you can retrieve it securely from your environment or other sources.
groq_api_key = st.secrets["groq_api_key"]

# Set up the page configuration for the Streamlit app
st.set_page_config(
    page_title='Groq Chatbot',   # Set the title of the web app
    page_icon='🤖',              # Add a robot emoji as the page icon
    layout='wide',               # Use a wide layout for more space
    initial_sidebar_state='expanded'  # Keep the sidebar expanded initially
)

# Function to initialize session state variables
def initialize_session_state():
    # Store the chat history in session state if not already present
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []   

    # Track the total number of messages
    if 'total_messages' not in st.session_state:
        st.session_state.total_messages = 0  

    # Track the session start time
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

# Function to get a custom prompt based on the selected persona
def get_custom_prompt():

    # Retrieve the selected persona from the session state, defaulting to 'Default' if none is selected
    persona = st.session_state.get('Selected persona', 'Default')

    # Define different persona templates for the chatbot
    personas = {

        'Default': """You are a friendly and helpful AI assistant, providing clear, concise, and accurate responses. 
                      Focus on being approachable and ensuring the user feels understood and supported.
                      Current conversation: 
                      {history} 
                      Human: {input}
                      AI:""",

        'Expert': """You are a highly knowledgeable and authoritative expert across various fields. 
                     Offer in-depth, precise, and technical explanations, citing examples or relevant research when necessary. 
                     Avoid jargon when possible, but feel free to introduce advanced concepts where appropriate. 
                     Current conversation: 
                     {history} 
                     Human: {input}
                     Expert:""",

        'Creative': """You are an imaginative and inventive AI with a flair for creative problem-solving and thinking outside the box. 
                       Use metaphors, vivid descriptions, and unconventional ideas to inspire and captivate the user. 
                       Feel free to suggest unique approaches or surprising solutions to problems.
                       Current conversation: 
                       {history} 
                       Human: {input}
                       Creative AI:"""
    }

    # Return a prompt template for the selected persona, replacing the variables {history} and {input}
    return PromptTemplate(
        input_variables=['history', 'input'],
        template=personas[persona]
    )


# Main function where all chatbot-related logic runs
def main():

    # Initialize session state variables
    initialize_session_state()

    # Sidebar setup for chat settings
    with st.sidebar:

        # Title for the sidebar with settings
        st.title('Configure Your Chat Experience ⚙️')

        # Model selection dropdown
        st.subheader('Select AI Model 🤖')
        model = st.selectbox(
            'Choose a model:', 
            ['llama3-70b-8192', 'gemma2-9b-it', 'mixtral-8x7b-32768'],
            help='Select the Large Language Model (LLM) for your conversation'
        )
        
        # Conversational memory length slider
        st.subheader('Set Conversation Memory 🔁')
        memory_length = st.slider(
            'Conversational Memory Length:', 
            1, 10, 5,
            help='Number of previous messages to be remembered'
        )
        
        # Persona selection dropdown
        st.subheader('Choose AI Personality 🎭')
        st.session_state.selected_persona = st.selectbox(
            'Select Conversation Style:',
            ['Default', 'Expert', 'Creative']
        )

        # Display chat statistics if the session has started
        if st.session_state.start_time:
            st.subheader('Conversation Overview 📊')
            col1, col2 = st.columns(2)
            
            # Column 1: Display number of messages
            with col1:
                st.metric('Total Messages Sent', len(st.session_state.chat_history))
            
            # Column 2: Display chat duration
            with col2:
                duration = datetime.now() - st.session_state.start_time
                st.metric('Session Duration', f'{duration.seconds // 60} minutes {duration.seconds % 60} seconds')
        
        # Button to clear chat history with an emoji
        if st.button('Clear All Chats and Start Fresh 🗑️', use_container_width=True):
            st.session_state.chat_history = []  # Reset chat history
            st.session_state.start_time = None  # Reset the start time
            st.rerun()  # Rerun the app to refresh the state

    # Set the title of the chatbot application with an emoji
    st.title('Groq AI Assistant 🤖')

    # Initialize the conversational memory buffer with the chosen memory length
    memory = ConversationBufferWindowMemory(k=memory_length)

    # Initialize the Groq chatbot with the selected model
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,  # You will need to define or retrieve this API key earlier in the script
        model_name=model            # Uses the selected model from the sidebar
    )

    # Set up the conversation chain with the selected LLM, memory, and custom persona prompt
    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory,
        prompt=get_custom_prompt()  # The custom prompt based on selected persona
    )

    # Load and replay previous chat history from session state memory
    for message in st.session_state.chat_history:
        # Save the context of past conversations to memory (human input and AI output)
        memory.save_context(
            {'input': message['human']},
            {'output': message['AI']}
        )

    # Display the chat history
    for message in st.session_state.chat_history:
        with st.container():
            # Show the human's message with an emoji
            st.write('You said 🗣️')
            st.info(message['human'])  # Display the human message with an info box

        with st.container():
            # Show the AI's response, indicating the selected persona mode with an emoji
            st.write(f'AI Assistant ({st.session_state.selected_persona} mode) replied 🤖')
            st.success(message['AI'])  # Display the AI response with a success box

        st.write('')  # Add an empty line for spacing between chat messages

    # User input section with an emoji
    st.markdown('What do you want to ask? 💬')  # Section heading
    user_question = st.text_area(
        '',                          # No label
        height=100,                  # Height of the text area
        placeholder='Ask me anything...',  # Placeholder text for the user input box
        key='user_input',            # Key to store the user input
        help='Type your question or message'      # Help tooltip
    )

    # Create three columns for the buttons
    col1, col2, col3 = st.columns([3, 1, 1])

    # Send button in the middle column with an emoji
    with col2:
        send_button = st.button('Send Message 🚀', use_container_width=True)

    # New Topic button in the last column to clear memory, with an emoji
    with col3:
        if st.button('Start New Conversation 🆕', use_container_width=True):
            memory.clear()  # Clear the conversation memory for a fresh topic
            st.success('Chat history has been cleared. Start a new conversation! 🔄')

    # If the user clicks 'Send' and there is a question in the input box
    if send_button and user_question:
        
        # Start timing the session if it's the user's first message
        if not st.session_state.start_time:
            st.session_state.start_time = datetime.now()

        # Display a spinner while processing the response
        with st.spinner('Processing your request... 🧠💡'):
            try:
                # Get the response from the conversation chain
                response = conversation(user_question)
                
                # Store the conversation in session state chat history
                message = {'human': user_question, 'AI': response['response']}
                st.session_state.chat_history.append(message)
                
                # Rerun the app to display the new message
                st.rerun()
            except Exception as e:
                # Show an error message if something goes wrong
                st.error(f'Error: {str(e)}')

    # Separator line between the chat and settings
    st.markdown('---')

    # Footer information about the current session, with dynamic persona and memory length info
    st.markdown(
    f'Chat powered by Groq AI in {st.session_state.selected_persona.lower()} mode | '
    f'Remembering the last {memory_length} messages'
    )

# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()
