import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
import pyttsx3
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import speech_recognition as sr

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

#Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

#speech Recognition
recognizer = sr.Recognizer()

#Function to Speak AI responce
def speak(text):
    try:
        # Initialize engine fresh each time to avoid threading issues with Streamlit
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)  # Set speaking rate
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        st.warning(f"⚠️ Text-to-speech failed: {str(e)}")
        # Fallback: just display the text
        pass

#Function to listen to voice input
def listen():
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None 

#define SI chat prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous conversation:\n{chat_history}\n\nUser: {question}\nAI:",
)

#Function to process AI Responce
def run_chain(question):
    #Retrieve chat history
    chat_history_text ="\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    #Run the AI Responce generation
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    # store new user input and AI response in memory
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    return response

#Streamlit web UI
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎤", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #9C27B0;
        font-size: 3em;
        margin-bottom: 0.3em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .user-msg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .ai-msg {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 20px 50px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎙️ Voice Assistant Info")
    st.write("**How to use:**")
    st.write("1. Click 'Start Talking' button")
    st.write("2. Speak your question clearly")
    st.write("3. Wait for AI response")
    st.write("4. Listen to the answer")
    st.markdown("---")
    st.write("**Model:** llama3.2:1b")
    st.write("**Features:**")
    st.write("🎤 Voice Input")
    st.write("🔊 Voice Output")
    st.write("💾 Conversation Memory")
    st.write("🧠 Context Awareness")
    
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.chat_history = ChatMessageHistory()
        st.rerun()

# Main title
st.markdown('<h1 class="main-title">🎤 AI Voice Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Speak naturally and get intelligent voice responses</p>', unsafe_allow_html=True)
st.markdown("---")

# Voice interaction section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎙️ Start Talking", use_container_width=True):
        user_query = listen()
        if user_query:
            with st.spinner("🤔 Processing your question..."):
                ai_response = run_chain(user_query)
            st.success("✅ Response ready!")
            speak(ai_response)

st.markdown("---")

# Display conversation history with styled messages
st.markdown("### 💬 Conversation History")

if len(st.session_state.chat_history.messages) == 0:
    st.info("🎙️ No conversations yet. Click 'Start Talking' to begin!")
else:
    for msg in st.session_state.chat_history.messages:
        if msg.type == "human":
            st.markdown(f'<div class="user-msg">👤 <strong>You said:</strong><br>{msg.content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-msg">🤖 <strong>AI responded:</strong><br>{msg.content}</div>', unsafe_allow_html=True)        