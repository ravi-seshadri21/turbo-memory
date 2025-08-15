from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai


# Set the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini pro model and generate response
model = genai.GenerativeModel("gemini-1.5-flash")     # Initialize the model
def get_gemini_pro_response(prompt):            # Function to get response from Gemini Pro model
    model = genai.GenerativeModel("gemini-1.5-flash") # Load the model
    response = model.generate_content(prompt)      # Generate text using the model
    return response.text                        # Return the generated text

# Streamlit app configuration
# Set page configuration
st.set_page_config(page_title="Gemini Pro Chatbot", page_icon=":robot_face:", layout="wide")
# Set header for the app
st.header("Gemini Pro Chatbot")
# Input text area for user prompt
# Text area for user input
input = st.text_input("Enter your prompt:", key="input")
# Submit button for user input
submit_button = st.button("Submit")
# Handle form submission
# Check if submit button is clicked and input is not empty
if submit_button:
    # Get response from Gemini Pro model
    response = get_gemini_pro_response(input)
    # Display response header
    st.write(response)