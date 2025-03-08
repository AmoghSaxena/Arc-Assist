import sys
import streamlit as st
import requests
import os




st.write(os.environ["LOGIN_STATUS"])
st.write(os.environ["API_KEY"])
st.write(os.environ["API_URL"])