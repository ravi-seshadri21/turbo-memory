from dotenv import load_dotenv
load_dotenv() ## Load all the environment variables
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

##Configure the Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load google gemini model and provide SQL query as response
def get_gemini_response(question,prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")  # Fixed class name
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to execute SQL query and return results
def read_sql_query(sql, db):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define your prompt
prompt = ["""You are an expert in SQL and you will be given a question. 
Your task is to provide a SQL query that answers the question.
The question will be related to a database of student with the following schema:
- Students: id, name, age, grade
- Courses: id, name, credits
- Enrollments: student_id, course_id, semester

Only return a valid SQL query. Do not include explanations or extra text.                   

"""]

def clean_sql_response(response):
    # Remove code block markers and language tags
    lines = response.strip().splitlines()
    cleaned_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(cleaned_lines).strip()

## Streamlit app
st.title("SQL Query Generator with Google Gemini")
st.set_page_config(page_title="SQL Query Generator", page_icon=":guardsman:", layout="wide")
question = st.text_input("Input:", key="input")
submit_button = st.button("Ask the question")

# If submit button is clicked
if submit_button:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL:")
    st.code(response, language="sql")  # Show the generated SQL

    try:
        data = read_sql_query(response, "student.db")
        st.subheader("The response is:")
        for row in data:
            st.write(row)
    except sqlite3.Error as e:
        st.error(f"SQL Error: {e}")

