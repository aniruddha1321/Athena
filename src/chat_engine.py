# chat_engine.py - Context-aware conversational AI for Athena
# Optimized with streaming and keep-alive for faster responses

import requests
from datetime import datetime
from typing import Generator, Optional
import hashlib


class AthenaChat:
    """Conversational AI with memory, PDF context awareness, streaming, and caching"""
    
    def __init__(self, model="llama3.2:1b", temperature=0.3):
        self.model = model
        self.temperature = temperature
        self.chat_history = []
        self.ollama_url = "http://localhost:11434/api/generate"
        self.pdf_context = None
        self._response_cache = {}  # Simple cache for repeated queries
    
    def set_pdf_context(self, pdf_text: str):
        """Set the PDF context for the chat session."""
        self.pdf_context = pdf_text
        self._response_cache.clear()  # Clear cache when context changes
        print(f"✅ PDF context set ({len(pdf_text)} characters)")
    
    def _get_cache_key(self, user_message: str) -> str:
        """Generate cache key for a message"""
        context_hash = hashlib.md5((self.pdf_context or "")[:1000].encode()).hexdigest()[:8]
        msg_hash = hashlib.md5(user_message.lower().strip().encode()).hexdigest()
        return f"{context_hash}_{msg_hash}"
    
    def chat_stream(self, user_message: str) -> Generator[str, None, None]:
        """
        Send a message and stream the response token by token.
        This provides real-time feedback to the user.
        
        Yields:
            Individual tokens/chunks as they arrive
        """
        # Check cache first
        cache_key = self._get_cache_key(user_message)
        if cache_key in self._response_cache:
            # Yield cached response all at once
            yield self._response_cache[cache_key]
            return
        
        try:
            # Build conversation context
            context = self._build_context()
            
            # Create prompt with history and PDF context
            if self.pdf_context:
                prompt = f"""You are Athena, an AI research assistant.

DOCUMENT:
{self.pdf_context[:1500]}

{context}

User: {user_message}
Athena:"""
            else:
                prompt = f"""You are Athena, an AI research assistant. You're knowledgeable, helpful, and professional.

{context}

User: {user_message}
Athena:"""
            
            # Call Ollama API with streaming enabled
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": 250,  # Reduced for speed
                    "num_ctx": 2048  # Balanced context
                },
                "keep_alive": "10m"  # Keep warm longer
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60, stream=True)
            
            if response.status_code != 200:
                yield f"❌ Error: {response.status_code}"
                return
            
            full_response = []
            
            # Stream response chunks
            for line in response.iter_lines():
                if line:
                    try:
                        import json
                        data = json.loads(line)
                        token = data.get("response", "")
                        if token:
                            full_response.append(token)
                            yield token
                        
                        # Check if done
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            # Save complete response to history and cache
            assistant_message = "".join(full_response).strip()
            
            if assistant_message:
                self.chat_history.append({
                    'timestamp': datetime.now(),
                    'user': user_message,
                    'assistant': assistant_message
                })
                # Cache the response
                self._response_cache[cache_key] = assistant_message
                
        except requests.exceptions.ConnectionError:
            yield "❌ Could not connect to Ollama. Make sure it's running: `ollama serve`"
        except requests.exceptions.Timeout:
            yield "❌ Request timed out. The model is taking too long to respond."
        except Exception as e:
            yield f"❌ Error: {str(e)}"
    
    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response (non-streaming, for compatibility).
        Uses streaming internally but returns complete response.
        """
        # Check cache first
        cache_key = self._get_cache_key(user_message)
        if cache_key in self._response_cache:
            return self._response_cache[cache_key]
        
        # Collect all streamed chunks
        response_parts = []
        for chunk in self.chat_stream(user_message):
            response_parts.append(chunk)
        
        return "".join(response_parts)
    
    def _build_context(self):
        """Build conversation context from history"""
        if not self.chat_history:
            return "This is the start of the conversation."
        
        # Include last 3 exchanges to keep context manageable
        recent = self.chat_history[-3:]
        context_lines = ["Previous conversation:"]
        
        for exchange in recent:
            context_lines.append(f"User: {exchange['user']}")
            context_lines.append(f"Athena: {exchange['assistant']}")
        
        return "\n".join(context_lines)
    
    def clear_history(self):
        """Clear conversation history"""
        self.chat_history = []
        self._response_cache.clear()
    
    def clear_pdf_context(self):
        """Clear PDF context"""
        self.pdf_context = None
        self._response_cache.clear()
    
    def get_history(self):
        """Get full conversation history"""
        return self.chat_history
    
    def export_history(self, filename="chat_history.txt"):
        """Export chat history to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Athena Chat History\n")
            f.write("=" * 50 + "\n\n")
            
            for i, exchange in enumerate(self.chat_history, 1):
                f.write(f"Exchange {i}\n")
                f.write(f"Time: {exchange['timestamp']}\n")
                f.write(f"User: {exchange['user']}\n")
                f.write(f"Athena: {exchange['assistant']}\n")
                f.write("-" * 50 + "\n\n")
        
        return filename


# Test function
if __name__ == "__main__":
    print("🧠 Testing Athena Chat Engine with Streaming\n")
    
    chat = AthenaChat()
    
    # Test streaming
    print("Testing streaming response:")
    print("User: Hello, who are you?")
    print("Athena: ", end="", flush=True)
    
    for token in chat.chat_stream("Hello, who are you?"):
        print(token, end="", flush=True)
    
    print("\n\n" + "-" * 60 + "\n")
    
    # Test with PDF context
    sample_pdf = """
    SAMPLE DOCUMENT
    
    This is a sample document about artificial intelligence.
    AI is transforming many industries including healthcare, finance, and education.
    Machine learning is a subset of AI that focuses on learning from data.
    """
    
    chat.set_pdf_context(sample_pdf)
    
    print("Testing with PDF context:")
    print("User: What industries is AI transforming?")
    print("Athena: ", end="", flush=True)
    
    for token in chat.chat_stream("What industries is AI transforming?"):
        print(token, end="", flush=True)
    
    print("\n")