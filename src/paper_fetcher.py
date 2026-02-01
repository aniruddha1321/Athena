# paper_fetcher.py - Fetch research papers from multiple sources

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import time
import os


@dataclass
class ResearchPaper:
    """Research paper metadata"""
    title: str
    authors: List[str]
    abstract: str
    year: int
    url: str
    pdf_url: Optional[str]
    source: str  # arxiv, semantic_scholar, pubmed
    citations: int = 0
    venue: str = ""
    
    def __str__(self):
        authors_str = ", ".join(self.authors[:3])
        if len(self.authors) > 3:
            authors_str += " et al."
        return f"{self.title}\n{authors_str} ({self.year})\n{self.abstract[:200]}..."


class PaperFetcher:
    """Fetch research papers from multiple academic sources"""
    
    def __init__(self):
        self.arxiv_base = "http://export.arxiv.org/api/query"
        self.semantic_scholar_base = "https://api.semanticscholar.org/graph/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Athena-Research-Assistant/1.0'
        })
    
    def search_papers(self, query: str, max_results: int = 10, 
                     sources: List[str] = None) -> List[ResearchPaper]:
        """
        Search for papers across multiple sources
        
        Args:
            query: Search query
            max_results: Maximum number of papers to fetch
            sources: List of sources to search ['arxiv', 'semantic_scholar']
                    If None, searches all available sources
        
        Returns:
            List of ResearchPaper objects
        """
        if sources is None:
            sources = ['arxiv', 'semantic_scholar']
        
        all_papers = []
        papers_per_source = max(5, max_results // len(sources))
        
        print(f"\n🔍 Searching for: '{query}'")
        print(f"📊 Target: {max_results} papers from {len(sources)} sources")
        
        # Search arXiv
        if 'arxiv' in sources:
            try:
                arxiv_papers = self._search_arxiv(query, papers_per_source)
                all_papers.extend(arxiv_papers)
                print(f"   ✅ arXiv: {len(arxiv_papers)} papers")
            except Exception as e:
                print(f"   ⚠️ arXiv error: {e}")
        
        # Search Semantic Scholar
        if 'semantic_scholar' in sources:
            try:
                ss_papers = self._search_semantic_scholar(query, papers_per_source)
                all_papers.extend(ss_papers)
                print(f"   ✅ Semantic Scholar: {len(ss_papers)} papers")
            except Exception as e:
                print(f"   ⚠️ Semantic Scholar error: {e}")
        
        # Remove duplicates based on title similarity
        all_papers = self._deduplicate_papers(all_papers)
        
        # Sort by citations (if available) and year
        all_papers.sort(key=lambda p: (p.citations, p.year), reverse=True)
        
        # Limit to max_results
        all_papers = all_papers[:max_results]
        
        print(f"📚 Total unique papers: {len(all_papers)}")
        
        return all_papers
    
    def _search_arxiv(self, query: str, max_results: int = 10) -> List[ResearchPaper]:
        """Search arXiv API"""
        import xml.etree.ElementTree as ET
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        response = self.session.get(self.arxiv_base, params=params, timeout=15)
        response.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        
        for entry in root.findall('atom:entry', namespace):
            # Extract data
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            
            # Authors
            authors = [
                author.find('atom:name', namespace).text 
                for author in entry.findall('atom:author', namespace)
            ]
            
            # Abstract
            summary = entry.find('atom:summary', namespace)
            abstract = summary.text.strip().replace('\n', ' ') if summary is not None else ""
            
            # Published date
            published = entry.find('atom:published', namespace).text
            year = int(published[:4])
            
            # Links
            pdf_url = None
            html_url = None
            
            for link in entry.findall('atom:link', namespace):
                if link.get('title') == 'pdf':
                    pdf_url = link.get('href')
                elif link.get('type') == 'text/html':
                    html_url = link.get('href')
            
            paper = ResearchPaper(
                title=title,
                authors=authors,
                abstract=abstract,
                year=year,
                url=html_url or pdf_url,
                pdf_url=pdf_url,
                source='arXiv',
                citations=0,  # arXiv doesn't provide citation counts
                venue='arXiv'
            )
            
            papers.append(paper)
            
            # Rate limiting
            time.sleep(0.1)
        
        return papers
    
    def _search_semantic_scholar(self, query: str, max_results: int = 10) -> List[ResearchPaper]:
        """Search Semantic Scholar API"""
        
        endpoint = f"{self.semantic_scholar_base}/paper/search"
        
        params = {
            'query': query,
            'limit': max_results,
            'fields': 'title,authors,abstract,year,url,citationCount,venue,openAccessPdf'
        }
        
        response = self.session.get(endpoint, params=params, timeout=15)
        
        if response.status_code == 429:
            print("   ⚠️ Rate limited, waiting...")
            time.sleep(2)
            response = self.session.get(endpoint, params=params, timeout=15)
        
        response.raise_for_status()
        data = response.json()
        
        papers = []
        
        for item in data.get('data', []):
            # Extract authors
            authors = [
                author.get('name', 'Unknown')
                for author in item.get('authors', [])
            ]
            
            # PDF URL
            pdf_info = item.get('openAccessPdf')
            pdf_url = pdf_info.get('url') if pdf_info else None
            
            paper = ResearchPaper(
                title=item.get('title', 'Untitled'),
                authors=authors,
                abstract=item.get('abstract', 'No abstract available'),
                year=item.get('year', 0),
                url=item.get('url', ''),
                pdf_url=pdf_url,
                source='Semantic Scholar',
                citations=item.get('citationCount', 0),
                venue=item.get('venue', '')
            )
            
            papers.append(paper)
            
            # Rate limiting
            time.sleep(0.1)
        
        return papers
    
    def _deduplicate_papers(self, papers: List[ResearchPaper]) -> List[ResearchPaper]:
        """Remove duplicate papers based on title similarity"""
        from difflib import SequenceMatcher
        
        unique_papers = []
        seen_titles = []
        
        for paper in papers:
            # Check if similar title already exists
            is_duplicate = False
            
            for seen_title in seen_titles:
                similarity = SequenceMatcher(None, paper.title.lower(), seen_title.lower()).ratio()
                if similarity > 0.85:  # 85% similarity threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_papers.append(paper)
                seen_titles.append(paper.title)
        
        return unique_papers
    
    def download_paper_pdf(self, paper: ResearchPaper, output_dir: str = ".") -> Optional[str]:
        """Download PDF of a paper"""
        import os
        
        if not paper.pdf_url:
            print(f"   ⚠️ No PDF available for: {paper.title[:50]}")
            return None
        
        try:
            # Create safe filename
            safe_title = "".join(c for c in paper.title[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}_{paper.year}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            print(f"   📥 Downloading: {paper.title[:50]}...")
            
            response = self.session.get(paper.pdf_url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   ✅ Saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"   ❌ Download failed: {e}")
            return None
    
    def format_papers_summary(self, papers: List[ResearchPaper]) -> str:
        """Format papers into a readable summary"""
        if not papers:
            return "No papers found."
        
        summary = f"# Research Papers on Your Topic\n\n"
        summary += f"Found {len(papers)} relevant papers:\n\n"
        summary += "---\n\n"
        
        for i, paper in enumerate(papers, 1):
            authors_str = ", ".join(paper.authors[:3])
            if len(paper.authors) > 3:
                authors_str += f" et al. ({len(paper.authors)} authors)"
            
            summary += f"## {i}. {paper.title}\n\n"
            summary += f"**Authors:** {authors_str}\n\n"
            summary += f"**Year:** {paper.year} | **Source:** {paper.source}"
            
            if paper.citations > 0:
                summary += f" | **Citations:** {paper.citations}"
            
            if paper.venue:
                summary += f" | **Venue:** {paper.venue}"
            
            summary += "\n\n"
            summary += f"**Abstract:** {paper.abstract}\n\n"
            
            summary += f"**Links:**\n"
            summary += f"- [View Paper]({paper.url})\n"
            if paper.pdf_url:
                summary += f"- [Download PDF]({paper.pdf_url})\n"
            
            summary += "\n---\n\n"
        
        return summary


# =====================================================================
# 🎯 MAIN RESEARCH FUNCTION
# =====================================================================

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def research_topic(topic: str, skip_tools: bool = False, fetch_papers: bool = True, 
                   max_papers: int = 5) -> str:
    """
    Research a topic by:
    1. Fetching relevant research papers from arXiv and Semantic Scholar
    2. Synthesizing the information using local LLM
    
    Args:
        topic: Research topic or query
        skip_tools: If True, skip paper fetching and just use LLM
        fetch_papers: Whether to fetch actual research papers
        max_papers: Maximum number of papers to fetch
    
    Returns:
        Comprehensive research summary
    """
    
    # Skip paper fetching for chunk summarization
    if skip_tools or not fetch_papers:
        return _generate_summary_only(topic)
    
    print(f"\n{'='*70}")
    print(f"🔬 RESEARCHING TOPIC: {topic}")
    print(f"{'='*70}\n")
    
    # Step 1: Fetch research papers
    print("📚 Step 1: Fetching research papers...")
    fetcher = PaperFetcher()
    
    try:
        papers = fetcher.search_papers(
            query=topic,
            max_results=max_papers,
            sources=['arxiv', 'semantic_scholar']
        )
        
        if not papers:
            print("⚠️ No papers found, generating summary from LLM knowledge...")
            return _generate_summary_only(topic)
        
        print(f"✅ Retrieved {len(papers)} papers\n")
        
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        print("⚠️ Falling back to LLM-only summary...")
        return _generate_summary_only(topic)
    
    # Step 2: Build context from papers
    print("📝 Step 2: Processing paper abstracts...")
    context = _build_research_context(papers)
    
    # Step 3: Generate comprehensive summary
    print("🧠 Step 3: Generating comprehensive analysis...\n")
    summary = _generate_research_summary(topic, papers, context)
    
    return summary


def _build_research_context(papers):
    """Build research context from papers"""
    
    context_parts = []
    
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors += " et al."
        
        context_parts.append(f"""
[Paper {i}] {paper.title}
Authors: {authors}
Year: {paper.year}
Source: {paper.source}
Citations: {paper.citations if paper.citations > 0 else 'N/A'}
Abstract: {paper.abstract}
""".strip())
    
    return "\n\n---\n\n".join(context_parts)


def _generate_research_summary(topic: str, papers, context: str) -> str:
    """Generate comprehensive research summary using LLM"""
    
    # Build paper list for reference
    paper_list = "\n".join([
        f"{i}. {paper.title} ({paper.year}) - {paper.authors[0]} et al."
        for i, paper in enumerate(papers, 1)
    ])
    
    prompt = f"""You are Athena, an expert AI research assistant. Analyze these recent research papers on "{topic}" and provide a comprehensive summary.

RESEARCH PAPERS:
{context}

Your task:
1. **Overview**: Provide a clear introduction to "{topic}" based on these papers
2. **Key Findings**: Summarize the main contributions and findings from each paper
3. **Common Themes**: Identify patterns, shared methodologies, or consensus across papers
4. **Recent Advances**: Highlight what's new or cutting-edge in this area
5. **Challenges & Future Work**: Discuss open problems and research directions mentioned
6. **Practical Impact**: Explain real-world applications and implications

Be specific and reference the papers by number [Paper 1], [Paper 2], etc.
Write in an academic yet accessible style. Aim for 800-1000 words.

PAPER REFERENCES:
{paper_list}

COMPREHENSIVE RESEARCH SUMMARY:"""

    try:
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 400,
                "num_ctx": 2048
            },
            "keep_alive": "10m"
        }
        
        print("   🤖 Calling Ollama API...")
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=180)
        
        if response.status_code != 200:
            print(f"   ❌ API Error: {response.status_code}")
            error_detail = ""
            try:
                error_json = response.json()
                if 'error' in error_json:
                    error_detail = f" - {error_json['error']}"
            except:
                pass
            print(f"   Error details: Status {response.status_code}{error_detail}")
            return _fallback_summary(papers)
        
        data = response.json()
        summary = data.get("response", "").strip()
        
        if not summary:
            print("   ⚠️ Empty response from LLM")
            return _fallback_summary(papers)
        
        # Add paper references at the end
        full_summary = f"{summary}\n\n{'='*70}\n\n## 📚 SOURCE PAPERS\n\n"
        
        for i, paper in enumerate(papers, 1):
            authors = ", ".join(paper.authors[:3])
            if len(paper.authors) > 3:
                authors += f" et al. ({len(paper.authors)} authors)"
            
            full_summary += f"\n**[Paper {i}]** {paper.title}\n"
            full_summary += f"- **Authors:** {authors}\n"
            full_summary += f"- **Year:** {paper.year} | **Source:** {paper.source}"
            
            if paper.citations > 0:
                full_summary += f" | **Citations:** {paper.citations}"
            
            full_summary += f"\n- **Link:** {paper.url}\n"
            
            if paper.pdf_url:
                full_summary += f"- **PDF:** {paper.pdf_url}\n"
        
        print("   ✅ Summary generated\n")
        return full_summary
        
    except requests.exceptions.Timeout:
        print("   ⏱️ Request timed out")
        return _fallback_summary(papers)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return _fallback_summary(papers)


def _generate_summary_only(topic: str) -> str:
    """Generate summary using only LLM knowledge (no paper fetching)"""
    
    prompt = f"""You are Athena, an expert AI research assistant. Provide a comprehensive overview of: "{topic}"

Include:
1. **Definition & Core Concepts**: What is this topic about?
2. **Key Methods & Techniques**: Main approaches used in this area
3. **Important Milestones**: Historical development and breakthroughs
4. **Current State**: What's the current state of research/practice?
5. **Applications**: Real-world use cases and impact
6. **Challenges**: Open problems and limitations
7. **Future Directions**: Where is this field heading?

Be specific, technical yet accessible. Aim for 600-800 words."""

    try:
        payload = {
            "model": "llama3.2:1b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.4,
                "num_predict": 300,
                "num_ctx": 2048
            },
            "keep_alive": "10m"
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Error generating summary").strip()
        else:
            error_msg = f"Error: API returned status {response.status_code}"
            try:
                error_detail = response.json()
                if 'error' in error_detail:
                    error_msg += f"\nDetails: {error_detail['error']}"
            except:
                error_msg += f"\nResponse: {response.text[:200]}"
            return error_msg
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model may be too busy or the prompt too long."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Please ensure Ollama is running with 'ollama serve'"
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def _fallback_summary(papers) -> str:
    """Fallback summary when LLM fails"""
    
    summary = "# Research Paper Summary\n\n"
    summary += f"Retrieved {len(papers)} relevant research papers:\n\n"
    summary += "---\n\n"
    
    for i, paper in enumerate(papers, 1):
        authors = ", ".join(paper.authors[:3])
        if len(paper.authors) > 3:
            authors += " et al."
        
        summary += f"## {i}. {paper.title}\n\n"
        summary += f"**Authors:** {authors}\n"
        summary += f"**Year:** {paper.year} | **Source:** {paper.source}"
        
        if paper.citations > 0:
            summary += f" | **Citations:** {paper.citations}"
        
        summary += f"\n\n**Abstract:**\n{paper.abstract}\n\n"
        summary += f"**Links:** [View Paper]({paper.url})"
        
        if paper.pdf_url:
            summary += f" | [PDF]({paper.pdf_url})"
        
        summary += "\n\n---\n\n"
    
    return summary


# =====================================================================
# 🧪 TEST SUITE
# =====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 RESEARCH PAPER FETCHER TEST")
    print("=" * 70)
    
    fetcher = PaperFetcher()
    
    # Test queries
    test_queries = [
        "transformer attention mechanism",
        "computer vision deep learning",
        "reinforcement learning robotics"
    ]
    
    query = test_queries[0]
    print(f"\n🔬 Testing with query: '{query}'")
    print("=" * 70)
    
    # Fetch papers
    papers = fetcher.search_papers(query, max_results=5)
    
    if papers:
        print(f"\n✅ Found {len(papers)} papers!\n")
        
        # Display papers
        for i, paper in enumerate(papers, 1):
            print(f"\n{i}. {paper.title}")
            print(f"   Authors: {', '.join(paper.authors[:2])}{'...' if len(paper.authors) > 2 else ''}")
            print(f"   Year: {paper.year} | Citations: {paper.citations} | Source: {paper.source}")
            print(f"   Abstract: {paper.abstract[:150]}...")
            print(f"   URL: {paper.url}")
            if paper.pdf_url:
                print(f"   PDF: {paper.pdf_url}")
        
        # Test summary formatting
        print("\n" + "=" * 70)
        print("📝 FORMATTED SUMMARY")
        print("=" * 70)
        
        summary = fetcher.format_papers_summary(papers[:3])
        print(summary[:500] + "...\n")
        
        # Test download (optional)
        print("=" * 70)
        print("💡 To test PDF download:")
        print("   paper = papers[0]")
        print("   fetcher.download_paper_pdf(paper)")
        
    else:
        print("❌ No papers found")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE!")
    print("=" * 70)
    
    print("\n💡 Usage in your code:")
    print("""
    from paper_fetcher import PaperFetcher
    
    fetcher = PaperFetcher()
    papers = fetcher.search_papers("your topic", max_results=10)
    
    # Get formatted summary
    summary = fetcher.format_papers_summary(papers)
    
    # Download PDFs
    for paper in papers:
        if paper.pdf_url:
            fetcher.download_paper_pdf(paper, output_dir="papers/")
    """)