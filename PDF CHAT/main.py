# ...existing code...
# Remove this line, it's not needed:
# from pdb import main

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# Read the PDF file and display its content
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Split the text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Create a vector store from the text chunks
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

# Get conversational chain
def get_conversational_chain():
    prompt_template = """
    You are a helpful AI assistant. 
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    Context:
    {context}

    Question:
    {question}

    Answer:
    {answer}
    
    """
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt_template)
    return chain

# User input and processing
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
            {"input_documents" : docs, "question" : user_question},
            return_only_outputs=True
        )
    print(response)
    # Use .get to avoid KeyError and show the actual output
    st.write(response.get('output_text', 'No response'))

def main():
    st.set_page_config(page_title="PDF Chatbot", page_icon=":robot_face:")
    st.title("PDF Chatbot")

    user_question = st.text_input("Ask a question about the PDF:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu: ")
        pdf_docs = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
        if st.button("Process PDFs"):
            with st.spinner("Processing PDFs..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.success("PDFs processed and vector store created!")

if __name__ == "__main__":
    main()