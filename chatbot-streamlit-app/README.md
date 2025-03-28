# Chatbot Streamlit App

This project is a Streamlit-based chatbot application that utilizes the `ArcAssistAPI` for backend interactions. The application provides a user-friendly interface for engaging with the chatbot and managing various functionalities.

## Project Structure

```
chatbot-streamlit-app
├── pages
│   └── 2_Chat.py          # Streamlit page for the chatbot interface
├── src
│   ├── api_anythingllm.py # API client for handling requests to the backend
│   └── utils.py           # Utility functions for the chatbot
├── requirements.txt        # Project dependencies
├── .streamlit
│   └── config.toml        # Streamlit configuration settings
├── README.md               # Project documentation
└── app.py                 # Main entry point for the Streamlit application
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd chatbot-streamlit-app
   ```

2. **Install dependencies:**
   It is recommended to create a virtual environment before installing the dependencies.
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   streamlit run app.py
   ```

## Usage Guidelines

- Navigate to the chatbot interface through the provided Streamlit app.
- Interact with the chatbot by typing your queries in the input field.
- The chatbot utilizes the `ArcAssistAPI` to process requests and provide responses.

## Additional Information

- Ensure that you have a valid API key for the `ArcAssistAPI` to enable full functionality.
- Modify the `src/utils.py` file to add any utility functions that may enhance the chatbot's capabilities.

For any issues or contributions, please refer to the project's GitHub page.