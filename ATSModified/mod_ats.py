import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import time
from dotenv import load_dotenv

load_dotenv() ##Load all the environment variables.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) ##Configure generative ai.
                
## Gemini Pro Response
def get_gemini_response(input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_prompt)
    return response.candidates[0].content.parts[0].text

##Extract Image from the PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text
    
## Prompt Template
input_prompt = """
You are a highly skilled and experienced Technical Human Resources Manager and an expert in ATS (Applicant Tracking Systems). 
Your task is to provide a comprehensive evaluation of the provided resume against the given job description.
The missing keywords with high accuracy and other key phrases which can be put in the resume to enhance the resume as per the job description provided.
resume: {text}
description: {jd}

Your response should be structured in the following sections:
1.  **Overall Score:** A single, clear percentage score indicating the resume's match with the job description.
2.  **Professional Summary:** A brief professional evaluation of the candidate's profile, highlighting their core strengths and weaknesses for the role.
3.  **Keyword Analysis:** A bulleted list of essential keywords missing from the resume, which are crucial for ATS visibility.
4.  **Actionable Suggestions:** Provide specific, actionable suggestions for improving the resume to better align with the job description and increase the ATS score.
{{"JD Match":"%", "Missing Keywords : []", "Profile Summary : ""}}
"""

## Streamlit App
st.title("Smart ATS")
st.text("This is to enhance and improve your ATS Resume")
jd=st.text_area("Provide the job description (optional)")
uploaded_file=st.file_uploader("Upload your resume", type='pdf', help="Please upload only pdf file format")
submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        start_time = time.time()
        text=input_pdf_text(uploaded_file)
        
        # Format the prompt with resume text and job description
        formatted_prompt = input_prompt.format(text=text, jd=jd)
        
        response=get_gemini_response(formatted_prompt)
        end_time = time.time()
        elapsed_time = end_time - start_time
        st.header(f"Time taken to generate the response: **{elapsed_time:.2f} seconds**")
        st.subheader(response)