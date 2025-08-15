from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state for chat history and chat object
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []  # List of dicts: {"role": ..., "parts": [...]}
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state['chat'] = model.start_chat(history=st.session_state['chat_history'])

def get_gemini_response(question):
    chat = st.session_state['chat']
    response = chat.send_message(question)
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Gemini ChatBot")
st.header("Gemini ChatBot in Gemini LLM Application")

input_text = st.text_input("Enter your question:", key="input")
submit_button = st.button("Click on Submit")

if submit_button and input_text:
    # Add user message to chat history
    st.session_state['chat_history'].append({"role": "user", "parts": [input_text]})
    # Send message and get response
    response_text = get_gemini_response(input_text)
    # Add Gemini response to chat history
    st.session_state['chat_history'].append({"role": "model", "parts": [response_text]})
    st.subheader("The Response from Gemini LLM is:")
    st.write(response_text)

st.subheader("The Chat History is:")
for msg in st.session_state['chat_history']:
    role = "You" if msg["role"] == "user" else "Gemini"
    st.write(f"{role}: {msg['parts'][0]}")