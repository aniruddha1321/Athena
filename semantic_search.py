# semantic_search.py — Debug version with detailed logging
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_semantic_index(pdf_text: str, chunk_size: int = 500, chunk_overlap: int = 100):
    """
    Build a FAISS semantic index from PDF text with smaller chunks for better precision.
    Returns the vectordb for searching.
    """
    try:
        print(f"🔧 Building index with chunk_size={chunk_size}, overlap={chunk_overlap}")
        print(f"📄 Input text length: {len(pdf_text)} characters")
        
        # Initialize embedding model
        embed_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        print("✅ Embedding model loaded")
        
        # Split text into smaller chunks for better granularity
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        texts = text_splitter.split_text(pdf_text)
        
        print(f"✂️ Split into {len(texts)} chunks")
        if texts:
            print(f"📝 First chunk preview: {texts[0][:100]}...")
        
        if not texts:
            raise ValueError("No text chunks created from PDF")
        
        # Create FAISS index
        vectordb = FAISS.from_texts(texts, embed_model)
        
        print(f"✅ Semantic index created with {len(texts)} chunks")
        return vectordb
        
    except Exception as e:
        print(f"❌ Error building semantic index: {e}")
        raise


def search_semantic(vectordb, query: str, k: int = 10):
    """
    Perform semantic search on the FAISS index.
    Returns ALL results without filtering.
    """
    try:
        print(f"\n🔍 Searching for: '{query}' (k={k})")
        
        if not query or not query.strip():
            print("⚠️ Empty query provided")
            return []
        
        # Perform similarity search with scores
        results = vectordb.similarity_search_with_score(query, k=k)
        print(f"📊 FAISS returned {len(results)} results")
        
        if not results:
            print("⚠️ No results from FAISS")
            return []
        
        # Debug: Print all distances
        distances = [score for _, score in results]
        print(f"📏 Distance range: min={min(distances):.4f}, max={max(distances):.4f}")
        
        # Return all results
        formatted_results = []
        for i, (doc, distance) in enumerate(results):
            print(f"   Result {i+1}: distance={distance:.4f}, text_len={len(doc.page_content)}")
            formatted_results.append((doc.page_content, distance))
        
        print(f"✅ Returning {len(formatted_results)} results")
        return formatted_results
        
    except Exception as e:
        print(f"❌ Error during semantic search: {e}")
        import traceback
        traceback.print_exc()
        raise