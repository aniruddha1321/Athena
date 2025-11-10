# tools/arxiv_search.py
from langchain_community.tools import Tool
from langchain_community.utilities import ArxivAPIWrapper


def search_arxiv(query: str, max_results: int = 3):
    """
    Search Arxiv for academic papers.
    Returns formatted results with titles, summaries, and URLs.
    """
    try:
        # Use LangChain's ArxivAPIWrapper for better error handling
        arxiv_wrapper = ArxivAPIWrapper(
            top_k_results=max_results,
            doc_content_chars_max=2000  # Limit summary length
        )
        
        results = arxiv_wrapper.run(query)
        
        if not results or results.strip() == "":
            return "No papers found on Arxiv for this query."
        
        return results
        
    except Exception as e:
        return f"Error searching Arxiv: {str(e)}"


# Create the tool
arxiv_tool = Tool(
    name="Arxiv Search",
    func=search_arxiv,
    description="Searches Arxiv for academic research papers. "
                "Returns paper titles, summaries, and URLs. "
                "Best for scientific and technical topics."
)


# Alternative: Direct arxiv library implementation (if you prefer more control)
def search_arxiv_direct(query: str, max_results: int = 3):
    """
    Direct implementation using arxiv library.
    Use this if ArxivAPIWrapper has issues.
    """
    try:
        import arxiv
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        client = arxiv.Client()
        
        for paper in client.results(search):
            result_text = (
                f"Title: {paper.title}\n"
                f"Authors: {', '.join(author.name for author in paper.authors)}\n"
                f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
                f"Summary: {paper.summary[:500]}...\n"
                f"URL: {paper.entry_id}\n"
            )
            results.append(result_text)
        
        if not results:
            return "No papers found on Arxiv for this query."
        
        return "\n\n---\n\n".join(results)
        
    except ImportError:
        return "Error: arxiv library not installed. Run: pip install arxiv"
    except Exception as e:
        return f"Error searching Arxiv: {str(e)}"


# Create alternative tool
arxiv_tool_direct = Tool(
    name="Arxiv Search Direct",
    func=search_arxiv_direct,
    description="Searches Arxiv for academic research papers using direct API access."
)


# Test function
if __name__ == "__main__":
    print("Testing Arxiv search...")
    result = search_arxiv("transformer neural networks")
    print(result)
    print("\n" + "="*80 + "\n")
    
    print("Testing direct Arxiv search...")
    result = search_arxiv_direct("attention mechanism deep learning")
    print(result)