#!/usr/bin/env python3
"""
Test script for Athena components
Run this to verify everything is working correctly
"""

import sys
import requests


def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("🔍 Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running")
            print(f"   Available models: {[m['name'] for m in models]}")
            
            if not any('llama3' in m['name'] for m in models):
                print("⚠️  Warning: llama3 model not found. Run: ollama pull llama3")
            return True
        else:
            print(f"❌ Ollama returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama at http://localhost:11434")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_imports():
    """Test if all required packages are installed"""
    print("\n📦 Testing imports...")
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("PyPDF2", "PyPDF2"),
        ("langchain", "langchain"),
        ("langchain_community", "langchain-community"),
        ("faiss", "faiss-cpu"),
        ("sentence_transformers", "sentence-transformers"),
        ("requests", "requests"),
        ("duckduckgo_search", "duckduckgo-search"),
        ("arxiv", "arxiv"),
    ]
    
    all_good = True
    for package_name, pip_name in required_packages:
        try:
            __import__(package_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name} - Run: pip install {pip_name}")
            all_good = False
    
    return all_good


def test_embeddings():
    """Test if sentence transformers can create embeddings"""
    print("\n🧮 Testing embeddings...")
    try:
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(["This is a test sentence"])
        
        print(f"✅ Embeddings working (dimension: {len(embeddings[0])})")
        return True
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return False


def test_faiss():
    """Test if FAISS vector store works"""
    print("\n🔍 Testing FAISS...")
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        
        embed = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        texts = ["Hello world", "How are you", "Testing FAISS"]
        vectordb = FAISS.from_texts(texts, embed)
        
        results = vectordb.similarity_search("hello", k=1)
        print(f"✅ FAISS working (found: '{results[0].page_content}')")
        return True
    except Exception as e:
        print(f"❌ FAISS error: {e}")
        return False


def test_qa_system():
    """Test the Q&A system"""
    print("\n💬 Testing Q&A system...")
    try:
        from qa_engine import make_qa_chain
        
        sample_text = """
        Artificial Intelligence (AI) is transforming the world.
        Machine learning is a subset of AI that focuses on learning from data.
        Deep learning uses neural networks with multiple layers.
        """
        
        print("   Building Q&A chain...")
        qa_function = make_qa_chain(sample_text, chunk_size=500, k=2, model="llama3")
        
        print("   Asking test question...")
        answer = qa_function("What is machine learning?")
        
        if answer and len(answer) > 10:
            print(f"✅ Q&A system working")
            print(f"   Answer preview: {answer[:100]}...")
            return True
        else:
            print(f"⚠️  Q&A returned short answer: {answer}")
            return False
            
    except Exception as e:
        print(f"❌ Q&A system error: {e}")
        return False


def test_semantic_search():
    """Test semantic search"""
    print("\n🔍 Testing semantic search...")
    try:
        from semantic_search import build_semantic_index, search_semantic
        
        sample_text = """
        Neural networks are computing systems inspired by biological neural networks.
        They consist of layers of interconnected nodes called neurons.
        Deep learning uses multiple layers to progressively extract features.
        """
        
        print("   Building semantic index...")
        vectordb = build_semantic_index(sample_text)
        
        print("   Searching...")
        results = search_semantic(vectordb, "what are neural networks", k=2)
        
        if results and len(results) > 0:
            print(f"✅ Semantic search working (found {len(results)} results)")
            print(f"   Top result: {results[0][0][:80]}...")
            return True
        else:
            print("⚠️  No results found")
            return False
            
    except Exception as e:
        print(f"❌ Semantic search error: {e}")
        return False


def test_web_search():
    """Test web search (optional - may be slow)"""
    print("\n🌐 Testing web search (optional)...")
    try:
        from tools.web_search import search_web
        
        result = search_web("Python programming", max_results=2)
        
        if result and "Error" not in result:
            print("✅ Web search working")
            return True
        else:
            print(f"⚠️  Web search issue: {result[:100]}")
            return False
    except Exception as e:
        print(f"⚠️  Web search not available: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧠 ATHENA SYSTEM TEST")
    print("=" * 60)
    
    results = []
    
    # Critical tests
    results.append(("Ollama Connection", test_ollama_connection()))
    results.append(("Package Imports", test_imports()))
    results.append(("Embeddings", test_embeddings()))
    results.append(("FAISS", test_faiss()))
    
    # Feature tests (only if critical tests pass)
    if all(r[1] for r in results):
        results.append(("Q&A System", test_qa_system()))
        results.append(("Semantic Search", test_semantic_search()))
        results.append(("Web Search", test_web_search()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Athena is ready to use.")
        print("   Run: streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())