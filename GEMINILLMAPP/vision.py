from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import io

# Set the Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model once
model = genai.GenerativeModel("gemini-2.5-pro")

def get_gemini_response(prompt, image_bytes):
    if image_bytes:
        # Prepare the image for the model
        image = Image.open(io.BytesIO(image_bytes))
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

# Streamlit app configuration
st.set_page_config(page_title="Gemini Pro Vision", page_icon=":robot_face:", layout="wide")
st.header("Gemini Pro Vision")

# Input text area for user prompt
prompt = st.text_input("Enter your prompt:", key="input")

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png", "heic"])

# Display the uploaded image
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Submit button for user input
submit_button = st.button("Submit")

if submit_button:
    image_bytes = uploaded_file.read() if uploaded_file else None
    response = get_gemini_response(prompt, image_bytes)
    st.write(response)