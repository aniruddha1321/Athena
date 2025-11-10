# main.py — Athena Core Logic (Hybrid Offline + Online Research)
# Works with LangChain 1.x+ and Ollama (llama3)

from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import ArxivAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests


def research_topic(topic: str, skip_tools=False):
    """
    Athena's hybrid research engine:
      - skip_tools=True  → purely local summarization (offline)
      - skip_tools=False → web research using DuckDuckGo + Arxiv + LLM reasoning
    """

    # 🧠 OFFLINE MODE — only uses local LLM
    if skip_tools:
        try:
            llm = ChatOllama(model="llama3", temperature=0.3)
            response = llm.invoke(topic)
            
            # Handle different response types
            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)
                
        except requests.exceptions.ConnectionError:
            return "⚠️ Error: Could not connect to Ollama. Make sure Ollama is running on http://localhost:11434"
        except Exception as e:
            return f"⚠️ Offline summarization error: {e}"

    # 🌐 ONLINE MODE — uses tools + reasoning chain
    try:
        llm = ChatOllama(model="llama3", temperature=0.3)
        
        # Define tools
        web_tool = DuckDuckGoSearchResults(num_results=5)
        
        # Use ArxivAPIWrapper for better compatibility
        arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=2000)
        
        # Perform web search
        web_results = ""
        try:
            web_results = web_tool.run(topic)
        except Exception as e:
            print(f"Web search error: {e}")
            web_results = "Web search unavailable."
        
        # Perform arxiv search
        arxiv_results = ""
        try:
            arxiv_results = arxiv_wrapper.run(topic)
        except Exception as e:
            print(f"Arxiv search error: {e}")
            arxiv_results = "Arxiv search unavailable."
        
        # Create comprehensive prompt with gathered information
        prompt = ChatPromptTemplate.from_template("""
You are Athena, a world-class AI research assistant.

User query: {input}

Web Search Results:
{web_results}

Academic Papers (Arxiv):
{arxiv_results}

Task: Synthesize the information from both sources and provide a comprehensive, 
academic-style summary of the topic. Include key findings, recent developments, 
and important research directions. Be concise but thorough.

If the sources don't contain relevant information, provide a general overview 
based on your knowledge, and mention that current sources were limited.
""")

        # Build chain
        chain = prompt | llm | StrOutputParser()
        
        # Invoke the chain
        result = chain.invoke({
            "input": topic,
            "web_results": web_results,
            "arxiv_results": arxiv_results
        })
        
        return result

    except requests.exceptions.ConnectionError:
        return "⚠️ Error: Could not connect to Ollama. Make sure Ollama is running on http://localhost:11434"
    except Exception as e:
        return f"⚠️ Online research error: {e}\n\nTrying offline mode..."


# Test function
if __name__ == "__main__":
    # Test offline mode
    print("Testing offline mode...")
    result = research_topic("Explain neural networks in simple terms", skip_tools=True)
    print(result)
    print("\n" + "="*80 + "\n")
    
    # Test online mode
    print("Testing online mode...")
    result = research_topic("Recent advances in transformer models", skip_tools=False)
    print(result)