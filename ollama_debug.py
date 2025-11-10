from langchain_ollama import OllamaLLM

print("🧠 Testing LangChain ↔ Ollama (modern API)...")

try:
    llm = OllamaLLM(model="llama3", temperature=0.2)
    response = llm.invoke("Explain what artificial intelligence is.")
    print("✅ Model responded successfully:")
    print(response)
except Exception as e:
    print("❌ Error communicating with Ollama:")
    print(e)
