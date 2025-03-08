import streamlit as st
import pandas as pd
import requests
import json
import os
import numpy as np
#import enviorment variables


def login(Authorization, API_URL):
    headers = {
        'accept': 'application/json',
        'Authorization': Authorization,
    }
    response = requests.get(f'{API_URL}/auth', headers=headers)
    return response




#print response with indentaion for better readability
if os.environ["LOGIN_STATUS"] == "1":
    API_KEY = st.text_input("Enter your API key", type="password") 
    API_URL = st.text_input("Enter the API URL", "https://arc.rexter.co.uk/api/v1")
    Authorization = f'Bearer {API_KEY}'

    if st.button("Login"):
        response = login(Authorization, API_URL)
        st.json(json.dumps(response.json(), indent=2))
        if response.status_code == 200:
            os.environ["LOGIN_STATUS"] = "0"
            os.environ["API_KEY"] = API_KEY
            os.environ["API_URL"] = API_URL
            st.success("Login successful")

else:
    if st.button("Logout"):
        os.environ["LOGIN_STATUS"] = "1"
        os.environ["API_KEY"] = "API"
        os.environ["API_URL"] = "API"
        LOGIN_STATUS = False
        st.success("Logout successful")