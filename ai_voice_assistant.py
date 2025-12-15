import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

#Initialize chat message history
chat_history = ChatMessageHistory()

#Initialize speech recognition and text-to-speech engines
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Set speaking rate

#speech Recognition
recognizer = sr.Recognizer()

#Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Function to Listen
def listen():
    with sr.Microphone() as source:
        print("Listening...")
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
    
#AI chat prompt
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous conversation:\n{chat_history}\n\nUser: {question}\nAI:",
)    

#Function to process AI Responce
def run_chain(question):
    #Retrieve chat history
    chat_history_text ="\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])
    #Run the AI Responce generation
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    # store new user input and AI response in memory
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)
    return response
#Main Loop
speak("Hello! I am your AI voice assistant. How can I help you today?")
while True:
    query = listen()
    if query:
        if 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break
        ai_response = run_chain(query)
        print("AI:", ai_response)
        speak(ai_response)