from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

#Load AI Model
llm = OllamaLLM(model="llama3.2:1b")

#Initialize chat message history
chat_history = ChatMessageHistory()

#Define AI chat prompt template
prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="Previous conversation:\n{chat_history}\n\nUser question: {question}\nAI:",
)

#Function to run AI chat with memory
def run_chain(question):
    #Retrieve chat history
    chat_history_text ="\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in chat_history.messages])
    #Run the AI Responce generation
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    # store new user input and AI response in memory
    chat_history.add_user_message(question)
    chat_history.add_ai_message(response)
    return response





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