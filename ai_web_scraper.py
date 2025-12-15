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
st.set_page_config(page_title="AI Web Scraper", page_icon="🌐", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FF6B6B;
        font-size: 3em;
        margin-bottom: 0.3em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .summary-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .content-preview {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🌐 Web Scraper Info")
    st.write("**How it works:**")
    st.write("1. Enter a valid website URL")
    st.write("2. Click 'Scrape & Summarize'")
    st.write("3. AI analyzes the content")
    st.write("4. Get intelligent summary")
    st.markdown("---")
    st.write("**Model:** llama3.2:1b")
    st.write("**Features:**")
    st.write("🌐 Web Content Extraction")
    st.write("📝 Smart Summarization")
    st.write("🤖 AI-Powered Analysis")
    st.write("⚡ Fast Processing")
    st.markdown("---")
    st.info("💡 **Tip:** Works best with news articles, blogs, and documentation pages.")

# Main title
st.markdown('<h1 class="main-title">🌐 AI Web Scraper</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Extract and summarize web content with AI intelligence</p>', unsafe_allow_html=True)
st.markdown("---")

# Input section
col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("🔗 Enter Website URL:", "", placeholder="https://example.com", label_visibility="visible")
with col2:
    st.write("")
    st.write("")
    scrape_button = st.button("🚀 Scrape & Summarize", use_container_width=True)

if url and (scrape_button or url):
    if url.startswith("http://") or url.startswith("https://"):
        with st.spinner("🔍 Fetching web content..."):
            content = scrape_web_page(url)
        
        if "Failed" in content or "error" in content:
            st.error(f"❌ {content}")
        else:
            # Show content preview
            with st.expander("📄 View Scraped Content Preview", expanded=False):
                st.markdown(f'<div class="content-preview">{content[:500]}...</div>', unsafe_allow_html=True)
            
            # Generate and display summary
            with st.spinner("🤔 AI is analyzing and summarizing..."):
                summary = summarize_content(content)
            
            st.success("✅ Summary generated successfully!")
            st.markdown("### 📊 AI-Generated Summary:")
            st.markdown(f'<div class="summary-box"><strong>Summary:</strong><br><br>{summary}</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a valid URL starting with http:// or https://")
    

            


