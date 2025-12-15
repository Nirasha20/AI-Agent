from langchain_ollama import OllamaLLM
#Load Ai modek from Ollama
llm = OllamaLLM(model="llama3.2:1b")
print("\n Welcome to your AI Agent! Ask me anything. Type 'exit' to quit.\n")
while True:
    question = input("Your question: ")
    if question.lower() == 'exit':
        print("Goodbye!")
        break
    response = llm.invoke(question)
    print("\nAI Response:", response)