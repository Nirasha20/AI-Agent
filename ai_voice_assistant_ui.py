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

#Initialize text-to-speech engines
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Set speaking rate 

#speech Recognition
recognizer = sr.Recognizer()

#Function to Speak AI responce
def speak(text):
    engine.say(text)
    engine.runAndWait()

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

#Streamlit web Ui
st.title("🤖AI Voice Assistant with Memory")
st.write("Click the button and speak to the AI voice assistant.")

#Button to start voice interaction 
if st.button("Start Talking"):
    user_query = listen()
    if user_query:
        ai_response = run_chain(user_query)
        st.write(f"**You**: {user_query}")
        st.write(f"**AI**: {ai_response}")
        speak(ai_response) 

#Display chat history
st.subheader("Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")        