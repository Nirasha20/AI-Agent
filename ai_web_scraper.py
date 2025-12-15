import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaLLM

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

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
        text = "\n".join([para.get_text() for para in paragraphs])

        return text[:2000]  # Limit to first 2000 characters for brevity
    except Exception as e:
        return f"An error occurred: {str(e)}"
#Function to generate summary using AI model
def summarize_content(content):
    st.write("Summarize content...")
    return llm.invoke(f"Summarize the following content:\n\n{content[:1000]}")
#Streamlit web UI
st.title("AI Web Scraper and Summarizer")
st.write("Enter a URL to scrape and summarize its content.")

#user input
url = st.text_input("Enter URL:", "")
if url:
    content = scrape_web_page(url)
    if "Failed" in content or "error" in content:
        st.write(content)
    else:
        summary = summarize_content(content)    
        st.subheader("Website Summary:")
        st.write(summary)
    

            


