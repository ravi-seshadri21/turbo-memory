import asyncio
import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS  # Assuming FAISS is used for vector storage
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Assuming GoogleGenerativeAIEmbeddings is used for embeddings

from dotenv import load_dotenv
load_dotenv()

# Ensure an event loop exists for the current thread (fix for "no current event loop" error)
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ...existing code...

# Load the Groq and Google Generative AI API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.title ("Gemma Model Chatbot, Document QA")

llm = ChatGroq(model_name="gemma2-9b-it", api_key=GROQ_API_KEY)

# Setup the prompt template
prompt_template = ChatPromptTemplate.from_template(
    """
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
)

# Create vector embeddings
def vector_embedding():

    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loaders = PyPDFDirectoryLoader("./in_census") ## Data ingestion
        st.session_state.docs = st.session_state.loaders.load() ## Load documents
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) ## Split documents into manageable chunks
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs) ## Split documents into manageable chunks
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings) ## Create vector embeddings

# Create a field for user input
# ...existing code...

prompt1 = st.text_input("Ask a question about the uploaded documents:", "")

if st.button("Vector Store"):
    vector_embedding()  # Create vector embeddings
    st.write("Vector embeddings created successfully!")

import time

if prompt1:
    if "vectors" not in st.session_state:
        st.warning("Please click the 'Vector Store' button to initialize the vector store before asking questions.")
    else:
        document_chain = create_stuff_documents_chain(llm, prompt_template)  # Create a chain for processing documents
        retriever = st.session_state.vectors.as_retriever()  # Create a retriever from the vector store
        retrieval_chain = create_retrieval_chain(retriever, prompt_template)  # Create a retrieval chain

        start = time.process_time()  # Start the timer
        response = retrieval_chain.invoke({"input": prompt1})  # Invoke the chain with the user question
        st.write("Response:", response["answer"])  # Display the response
        end = time.process_time()  # End the timer

        # With a streamlit expander, you can show the response time
        with st.expander("Response Time"):
            # Find the relevant chunks of text
            for i, doc in enumerate(response["context"]):  # Iterate through the context documents
                st.write(doc.page_content)  # Display the content of each document
                st.write(f"Response Time: {end - start} seconds")  # Display the response time