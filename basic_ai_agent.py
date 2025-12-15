import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")
#Initialize chat message history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

#Define AI chat prompt template
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are a helpful AI assistant. Use the previous conversation context to provide relevant responses.

Previous conversation:
{chat_history}

User: {question}
AI Assistant:""",
)    
#Function to run AI chat with memory
def run_chain(question):
    #Retrieve chat history
    chat_history_text ="\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])


    #Run the AI Responce generation
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))

    # store new user input and AI response in memory
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    return response


# Streamlit UI
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #4A90E2;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .user-msg {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #2196F3;
    }
    .ai-msg {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #4CAF50;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This AI chatbot remembers your conversation history and provides contextual responses.")
    st.write("**Model:** llama3.2:1b")
    st.write("**Features:**")
    st.write("✓ Conversation memory")
    st.write("✓ Context-aware responses")
    st.write("✓ Chat history tracking")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = ChatMessageHistory()
        st.rerun()

# Main title
st.markdown('<h1 class="main-title">🤖 AI Chatbot Assistant</h1>', unsafe_allow_html=True)
st.markdown("---")

# Chat container
chat_container = st.container()

with chat_container:
    if len(st.session_state.chat_history.messages) == 0:
        st.info("👋 Hello! I'm your AI assistant. Ask me anything to get started!")
    else:
        for msg in st.session_state.chat_history.messages:
            if msg.type == "human":
                st.markdown(f'<div class="user-msg">👤 <strong>You:</strong><br>{msg.content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-msg">🤖 <strong>AI:</strong><br>{msg.content}</div>', unsafe_allow_html=True)

# Input section at bottom
st.markdown("---")

# Use a form to prevent continuous submission
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input("💬 Type your message here:", "", key="user_input", label_visibility="collapsed", placeholder="Type your question and press Enter...")
    
    with col2:
        send_button = st.form_submit_button("Send 📤", use_container_width=True)

if send_button and user_input:
    with st.spinner("🤔 Thinking..."):
        response = run_chain(user_input)
        st.rerun()     

# Show full chat history
st.subheader("📜 Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(f"**{msg.type.capitalize()}**: {msg.content}")


















###Basic AI Agent with Memory

# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.prompts import PromptTemplate
# from langchain_ollama import OllamaLLM

# #Load AI Model
# llm = OllamaLLM(model="llama3.2:1b")

# #Initialize chat message history
# chat_history = ChatMessageHistory()

# #Define AI chat prompt template
# prompt = PromptTemplate(
#     input_variables=["chat_history", "question"],
#     template="Previous conversation:\n{chat_history}\n\nUser question: {question}\nAI:",
# )

# #Function to run AI chat with memory
# def run_chain(question):
#     #Retrieve chat history
#     chat_history_text ="\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])
#     #Run the AI Responce generation
#     response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
#     # store new user input and AI response in memory
#     chat_history.add_user_message(question)
#     chat_history.add_ai_message(response)
#     return response

# #interactive CLI Chatbot
# print("\n AI chatbot with Memory")
# print("Type 'exit' to quit.\n ")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == 'exit':
#         print("Goodbye!")
#         break
#     ai_responce = run_chain(user_input)
#     print("AI:", ai_responce)







#from langchain_ollama import OllamaLLM
#Load Ai modek from Ollama
#llm = OllamaLLM(model="llama3.2:1b")
#print("\n Welcome to your AI Agent! Ask me anything. Type 'exit' to quit.\n")
#while True:
  #  question = input("Your question: ")
   # if question.lower() == 'exit':
    #    print("Goodbye!")
    #    break
    #response = llm.invoke(question)
    #print("\nAI Response:", response)