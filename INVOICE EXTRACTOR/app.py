from dotenv import load_dotenv
load_dotenv() ## Load environment variables from .env file.
    
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

## Function to load Gemini vision model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [

            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded. Please upload an image file.")
    
## Initialize Streamlit app
st.set_page_config(page_title="Invoice Extractor")

st.header("Invoice Extractor")
input = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"]) 
image=" "
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)


submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understandin invoices.
We will upload an image as invoice and you will have to analyse the image.
"""
## If submit button is clicked or Enter key is pressed
if submit or st.session_state.get("input"):
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input, image_data, input_prompt)
    st.subheader("The response is ")
    st.write(response)