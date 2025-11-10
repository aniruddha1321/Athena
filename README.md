# 🧠 Athena - AI Research Assistant

A powerful local AI research assistant powered by Ollama and LangChain. Athena helps you analyze research papers, perform semantic search, and get intelligent answers from PDFs.

## ✨ Features

- 📄 **PDF Analysis**: Upload and analyze research papers
- 💬 **Q&A System**: Ask questions about uploaded documents
- 🔍 **Semantic Search**: Find relevant sections using natural language
- 🌐 **Web Research**: Search the web and academic papers (Arxiv)
- 🤖 **Local LLM**: Powered by Ollama (completely offline capable)
- 🎨 **Modern UI**: Clean Streamlit interface

## 🚀 Installation

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

```bash
# Pull the Llama 3 model
ollama pull llama3
```

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd athena
```

### 3. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Start Ollama Server

```bash
ollama serve
```

### Run Athena

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Upload a PDF
- Click "Choose a PDF file" and upload a research paper
- Click "✨ Research" to analyze the paper

### 2. Ask Questions (Q&A Tab)
- Switch to the "💬 Q&A" tab
- Type your question in the input box
- Click "Ask" to get answers from the paper

### 3. Semantic Search (Search Tab)
- Switch to the "🔍 Semantic Search" tab
- Enter keywords or phrases to search
- View relevant sections ranked by similarity

### 4. Web Research (Optional)
- Enter a topic in the research input
- Click "✨ Research" without uploading a PDF
- Athena will search the web and Arxiv for information

## 🛠️ Project Structure

```
athena/
├── app.py                 # Main Streamlit application
├── main.py               # Research logic (online/offline)
├── qa_engine.py          # Q&A system with FAISS
├── semantic_search.py    # Semantic search functionality
├── tools/
│   ├── arxiv_search.py  # Arxiv paper search
│   └── web_search.py    # DuckDuckGo web search
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Change the LLM Model

Edit `app.py`, `qa_engine.py`, and `main.py`:

```python
# Change from llama3 to another model
model="mistral"  # or "llama2", "codellama", etc.
```

### Adjust Chunk Sizes

In `qa_engine.py` and `semantic_search.py`:

```python
chunk_size=2000      # Size of text chunks
chunk_overlap=200    # Overlap between chunks
k=5                  # Number of results to retrieve
```

## 🐛 Troubleshooting

### "Could not connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`
- Verify the URL: `http://localhost:11434`

### "No text extracted from PDF"
- The PDF might be scanned (image-based)
- Try using OCR tools or a different PDF
- Check if the PDF is encrypted

### "Import errors"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Slow performance
- Use a smaller model: `ollama pull llama2:7b`
- Reduce chunk_size in the code
- Reduce the number of results (k parameter)

## 📦 Dependencies

### Core
- Python 3.8+
- Streamlit
- LangChain
- Ollama

### ML/AI
- FAISS (vector search)
- sentence-transformers (embeddings)

### Search Tools
- duckduckgo-search
- arxiv

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local LLM runtime
- [LangChain](https://langchain.com) - LLM framework
- [Streamlit](https://streamlit.io) - Web framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search

## 📧 Support

If you encounter any issues, please open an issue on GitHub.

---

Built with ❤️ using Ollama and LangChain