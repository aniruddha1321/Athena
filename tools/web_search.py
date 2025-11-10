# tools/web_search.py
from langchain_community.tools import Tool


def search_web(query: str, max_results: int = 5):
    """
    Search the web using DuckDuckGo.
    Returns formatted results with titles, snippets, and URLs.
    """
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "No relevant web results found for this query."
        
        # Format results nicely
        formatted = []
        for i, r in enumerate(results, 1):
            title = r.get('title', 'No title')
            body = r.get('body', 'No description')
            href = r.get('href', 'No URL')
            
            formatted.append(f"{i}. {title}\n   {body}\n   URL: {href}")
        
        return "\n\n".join(formatted)
        
    except ImportError:
        return "Error: duckduckgo-search library not installed. Run: pip install duckduckgo-search"
    except Exception as e:
        return f"Error during web search: {str(e)}"


# Alternative: Use LangChain's built-in DuckDuckGo tool
def search_web_langchain(query: str):
    """
    Use LangChain's DuckDuckGoSearchResults tool.
    This is more reliable and better integrated with LangChain.
    """
    try:
        from langchain_community.tools import DuckDuckGoSearchResults
        
        search_tool = DuckDuckGoSearchResults(num_results=5)
        results = search_tool.run(query)
        
        if not results or results.strip() == "":
            return "No relevant web results found for this query."
        
        return results
        
    except ImportError:
        return "Error: Required libraries not installed. Run: pip install duckduckgo-search"
    except Exception as e:
        return f"Error during web search: {str(e)}"


# Create the tool (using custom implementation)
web_search_tool = Tool(
    name="Web Search",
    func=search_web,
    description="Searches the web using DuckDuckGo for recent articles, news, blogs, and general information. "
                "Returns titles, descriptions, and URLs of relevant web pages."
)


# Alternative LangChain-based tool
web_search_tool_langchain = Tool(
    name="Web Search LangChain",
    func=search_web_langchain,
    description="Searches the web for recent articles, blogs, or papers using DuckDuckGo."
)


# Test function
if __name__ == "__main__":
    print("Testing custom web search...")
    result = search_web("latest AI research 2025")
    print(result)
    print("\n" + "="*80 + "\n")
    
    print("Testing LangChain web search...")
    result = search_web_langchain("transformer models recent developments")
    print(result)