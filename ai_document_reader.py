import streamlit as st
import faiss
import numpy as np
from pypdf import PdfReader
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

#Load huggingface embedding model
embedding_model =HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#Initialize FAISS vector Database
index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2 is 384
vector_store = {}  
summary_text = "" 
#Function to process PDF document
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

#function to store data in FAISS
def store_in_faiss(text, filename):
    global index, vector_store
    st.write("Storing data in FAISS vector store...")
    
    #Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = splitter.split_text(text)

    #convert texts to embeddings
    vectors = embedding_model.embed_documents(texts)
    vectors = np.array(vectors).astype(np.float32)

    #store in FAISS
    index.add(vectors)
    vector_store[len(vector_store)] = (filename, texts)

    return "Data stored successfully."

#Function to generate AI summary
def generate_summary(text):
    global summary_text
    st.write("Generating summary...")
    summary_text = llm.invoke(f"Summarize the following document content:\n\n{text[:3000]}")
    return summary_text

#function to retrieve relevant info from FAISS
def retrieve_and_answer(query):
    global index, vector_store
    
    #Convert query to embedding
    query_vector = np.array(embedding_model.embed_query(query)).astype(np.float32).reshape(1, -1)

    #Search in FAISS
    D, I = index.search(query_vector, k=2)  # Retrieve top 2 relevant chunks
    context = ""
    for idx in I[0]:
        # Skip invalid indices (FAISS returns -1 for no match)
        if idx >= 0 and idx < len(vector_store):
            context += "\n".join(vector_store[idx][1]) + "\n\n"

    if not context:
        return "No relevant information found in the document."
    
    #Ask AI to generate an answer using the context
    return llm.invoke(f"Using the following context from the document, answer the question:\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:") 

#Function to allow file download
def download_summary():
    st.download_button(
        label="Download Summary",
        data=summary_text,
        file_name="AI_Summary.txt",
        mime="text/plain"
    )
           
            
#streamlit web UI
st.title("📄 AI Document Reader with FAISS")
st.write("Upload a PDF and get an AI-generated summary and Q&A capabilities.")

#File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    store_message = store_in_faiss(text, uploaded_file.name)
    st.write(store_message)

    #Generate AI summary
    summary = generate_summary(text)
    st.subheader("**AI-Generated Summary:**")
    st.write(summary)

    #Enable file download for summary
    download_summary()
#User input for questions
query = st.text_input("Ask a question based on the uploaded document:", "")
if query:
    answer = retrieve_and_answer(query)
    st.subheader("**AI Answer:**")
    st.write(answer)

