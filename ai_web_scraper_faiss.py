import requests
from bs4 import BeautifulSoup
import streamlit as st
import faiss
import numpy as np
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter   
from langchain_core.documents import Document

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

#Load Embedding Model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#Initialize FAISS vector store
index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2 is 384
vector_store = {}

#Function to scrape web page content
def scrape_web_page(url):
    try:
        st.write(f"Scraping content from: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return f"Failed to fetch {url}"
        
        #Extract text content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')   
        paragraphs = soup.find_all('p')
        text = "\n".join([p.get_text() for p in paragraphs])

        return text[:5000]  # Limit to first 5000 characters for brevity
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
#Function to store data in FAISS
def store_in_faiss(text, url):
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
    vector_store[len(vector_store)] = (url, texts)

    return "Data stored successfully."
#Function to retrieve relevant info from FAISS
def retrieve_and_answer(query):
    global index, vector_store

    #Convert query into embedding
    query_vector = np.array(embedding_model.embed_query(query)).astype(np.float32).reshape(1, -1)

    #Search FAISS for similar vectors
    D, I = index.search(query_vector, k=2)  # Retrieve top

    context = ""
    for idx in I[0]:
        if idx in vector_store:
            context += "\n".join(vector_store[idx][1]) + "\n\n"

            if not context:
                return "No relevant information found in the vector store."
            
            #Ask AI to generate an answer
            return llm.invoke(f"Using the following context, answer the question:\n\nContext:\n{context}\n\nQuestion: {query}")
#Streamlit web UI
st.title("🌐 AI Web Scraper with FAISS Vector Store")
st.write("Enter a website URL below and store its knowledge for AI-based Q&A.")
#User input for website
url = st.text_input("Website URL:", "")
if url:
    content = scrape_web_page(url)
    if "Failed" in content or "error" in content:
        st.write(content)
    else:
        
        store_message = store_in_faiss(content, url)
        st.write(store_message)

#User input for questions
query = st.text_input("Ask a question based on stored web content:",) 
if query:
    answer = retrieve_and_answer(query)
    st.subheader("**AI Answer:**")
    st.write(answer)       