# qa_engine.py — Fixed for LangChain 0.3+ compatibility
# Optimized with streaming and keep-alive for faster responses

import streamlit as st
import requests
from typing import Generator
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

OLLAMA_URL = "http://localhost:11434/api/generate"


def make_qa_chain(pdf_text: str, chunk_size: int = 2000, k: int = 3, model: str = "llama3.2:1b"):
    """
    Offline Q&A system using local Ollama API for LLM inference.
    Returns a callable function that answers questions with streaming support.
    
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

    def answer_stream(question: str) -> Generator[str, None, None]:
        """Answer questions with streaming response"""
        try:
            # Retrieve most relevant context
            try:
                docs = retriever.invoke(question)
            except AttributeError:
                docs = retriever.get_relevant_documents(question)
            
            if not docs:
                yield "⚠️ No relevant context found in the document."
                return
            
            context = "\n\n---\n\n".join([doc.page_content for doc in docs])
            
            # Build prompt
            prompt = f"""You are Athena, an intelligent AI research assistant.
Answer the question based strictly on the provided context below.
If the context doesn't contain enough information, say: "I don't have enough information from this document to answer that question."

Context:
{context}

Question: {question}

Answer:"""
            
            # Send request to Ollama API with streaming
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 250,  # Reduced for speed
                    "num_ctx": 2048  # Balanced context
                },
                "keep_alive": "10m"
            }
            
            response = requests.post(OLLAMA_URL, json=payload, timeout=60, stream=True)
            
            if response.status_code != 200:
                yield f"❌ Ollama API error {response.status_code}: {response.text}"
                return
            
            # Stream response chunks
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            yield token
                        
                        if data.get("done", False):
                            break
                    except:
                        continue
            
        except requests.exceptions.Timeout:
            yield "❌ Request timed out. The model might be processing a large context."
        except requests.exceptions.ConnectionError:
            yield "❌ Could not connect to Ollama. Make sure it's running on http://localhost:11434"
        except Exception as e:
            yield f"❌ Error during Q&A: {str(e)}"

    def answer(question: str) -> str:
        """Answer questions (non-streaming for backwards compatibility)"""
        response_parts = []
        for chunk in answer_stream(question):
            response_parts.append(chunk)
        return "".join(response_parts).strip()
    
    # Return function with both methods accessible
    answer.stream = answer_stream
    return answer