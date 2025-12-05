# qa_engine.py — Fixed for LangChain 0.3+ compatibility
import streamlit as st
import requests
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

OLLAMA_URL = "http://localhost:11434/api/generate"


def make_qa_chain(pdf_text: str, chunk_size: int = 2000, k: int = 3, model: str = "llama3.2:1b"):
    """
    Offline Q&A system using local Ollama API for LLM inference.
    Returns a callable function that answers questions.
    
    Compatible with LangChain 0.3+ (uses invoke() instead of get_relevant_documents())
    """
    
    try:
        # 1️⃣ Create vector embeddings
        embed = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2️⃣ Split text into chunks properly
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            length_function=len,
        )
        texts = text_splitter.split_text(pdf_text)
        
        if not texts:
            raise ValueError("No text chunks created from PDF")
        
        # 3️⃣ Create FAISS index
        vectordb = FAISS.from_texts(texts, embed)
        retriever = vectordb.as_retriever(search_kwargs={"k": k})
        
        print(f"✅ QA Index created with {len(texts)} chunks")
        
    except Exception as e:
        print(f"❌ Error creating QA index: {e}")
        raise

    def answer(question: str) -> str:
        """Answer questions based on the PDF content"""
        try:
            # Retrieve most relevant context using invoke() for LangChain 0.3+
            # Try both methods for compatibility
            try:
                # Method 1: invoke() (LangChain 0.3+)
                docs = retriever.invoke(question)
            except AttributeError:
                # Method 2: get_relevant_documents() (older versions)
                docs = retriever.get_relevant_documents(question)
            
            if not docs:
                return "⚠️ No relevant context found in the document."
            
            context = "\n\n---\n\n".join([doc.page_content for doc in docs])
            
            # Build prompt
            prompt = f"""You are Athena, an intelligent AI research assistant.
Answer the question based strictly on the provided context below.
If the context doesn't contain enough information, say: "I don't have enough information from this document to answer that question."

Context:
{context}

Question: {question}

Answer:"""
            
            # Send request to Ollama API
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 500
                }
            }
            
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            
            if response.status_code != 200:
                return f"❌ Ollama API error {response.status_code}: {response.text}"
            
            data = response.json()
            answer_text = data.get("response", "").strip()
            
            if not answer_text:
                return "⚠️ No answer received from the model."
            
            return answer_text
            
        except requests.exceptions.Timeout:
            return "❌ Request timed out. The model might be processing a large context."
        except requests.exceptions.ConnectionError:
            return "❌ Could not connect to Ollama. Make sure it's running on http://localhost:11434"
        except Exception as e:
            return f"❌ Error during Q&A: {str(e)}"
    
    return answer