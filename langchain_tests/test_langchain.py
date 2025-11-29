from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Local Ollama model
model = ChatOllama(
    model="gemma3:4b",
    base_url="http://localhost:11434"
)

print("LangChain + Ollama chat started. Type 'exit' to quit.\n")

while True:
    user = input("You: ")
    if user.lower() in ["exit", "quit"]:
        break

    response = model.invoke([HumanMessage(content=user)])
    print("AI:", response.content)
