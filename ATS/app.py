from dotenv import load_dotenv
import os
import streamlit as st
import base64
import io
import pdf2image
from PIL import Image
import google.generativeai as genai
import time

# Load environment variables and configure genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Ensure all inputs are strings
    question = str(question)
    prompt = str(prompt)
    
    # Prepare the content for the model
    content = [question, pdf_content, prompt]
    
    response = model.generate_content(content)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        return first_page
    else:
        raise FileNotFoundError("No file uploaded")
    
# Create the Streamlit app
st.set_page_config(page_title="ATS Resume Expert", page_icon=":book:")
st.header("ATS Resume Tracking Expert")
input_text = st.text_area("Enter the job description here :", key='input')
uploaded_file = st.file_uploader("Upload your resume in any file format", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Which Keywords Should I Use?, Which are Missing here as per the job description?")
submit4 = st.button("What is the Overall Score of my Resume?")

input_prompt1 = """
    You are an experienced Technical Human Resource Manager in any one of the field involving Data Science, Full Stack Web Development, Big Data, Data Engineering, DEVOPS, Data Analyst, 
    your task is to review the provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
    You are an experienced Technical Human Resource Manager in any one of the field involving Data Science, Full Stack Web Development, Big Data, Data Engineering, DEVOPS, Data Analyst,
    your task is to scrutinize the provided resume against the job description.
    Please share your insights on whether the candidate's profile is suitable for the role.
    Provide the relevant skills of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
    You are an experienced Technical Human Resource Manager in any one of the field involving Data Science, Full Stack Web Development, Big Data, Data Engineering, DEVOPS, Data Analyst, 
    your task is to review the provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the missing keywords of the applicant in relation to the specified job requirements.
"""

input_prompt4 = """
    You are a skilled ATS System scanner with a deep understanding of resume evaluation, Data Science and ATS functionality.
    Your task is to analyze the provided resume and job description and provide us results in the form of percentage.
    Please share your insights on how well the resume matches the job requirements.
"""

if submit1:
    if uploaded_file is not None:
        start_time = time.time()
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(response)
        st.header(f"Time taken to generate the response: **{elapsed_time:.2f} seconds**")
    else:
        st.write("Please upload a resume file to proceed.")

elif submit2:
    if uploaded_file is not None:
        start_time = time.time()
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(response)
        st.header(f"Time taken to generate the response: **{elapsed_time:.2f} seconds**")
    else:
        st.write("Please upload a resume file to proceed.")

elif submit3:
    if uploaded_file is not None:
        start_time = time.time()
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(response)
        st.header(f"Time taken to generate the response: **{elapsed_time:.2f} seconds**")
    else:
        st.write("Please upload a resume file to proceed.")

elif submit4:
    if uploaded_file is not None:
        start_time = time.time()
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.write(response)
        st.header(f"Time taken to generate the response: **{elapsed_time:.2f} seconds**")
    else:
        st.write("Please upload a resume file to proceed.")