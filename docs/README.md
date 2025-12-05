# 🧠 Athena - AI Research Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io)

> A powerful local AI research assistant powered by Ollama and LangChain. Analyze research papers, build knowledge graphs, perform multi-document reasoning, and more—all running locally on your machine.

![Athena Demo](https://via.placeholder.com/800x400?text=Athena+Demo+Screenshot)

## ✨ Features

### 🎯 Core Research Tools
- **📄 Document Summarization** - Intelligent multi-section summarization
- **💬 Q&A System** - RAG-based question answering with context
- **🔍 Semantic Search** - Find relevant sections using natural language
- **🤖 Chat Interface** - Conversational AI with document context
- **📊 Document Comparison** - Deep comparative analysis of multiple papers

### 🚀 Advanced Features
- **🕸️ Knowledge Graph Construction** - Automatically extract and visualize entities, relationships, and concepts
- **📚 Multi-Document RAG** - Cross-paper reasoning with source attribution and confidence scoring
- **🎤 Voice Interface** - Speech-to-text and text-to-speech capabilities
- **📈 Performance Metrics** - Track entity relationships and concept evolution

### 💡 Use Cases
- 📚 **Literature Reviews** - Compare and synthesize multiple papers
- 🔬 **Research Analysis** - Extract entities, methods, and results
- 🎓 **Academic Writing** - Find relevant citations and connections
- 🧪 **Paper Understanding** - Visual knowledge graphs and contextual Q&A

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should show 3.8+
   ```

2. **Ollama** (for local LLM)
   - Download from [ollama.ai](https://ollama.ai)
   - Install and run:
   ```bash
   ollama pull llama3
   ollama serve
   ```

### Installation

#### Option 1: Automated Setup (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/yourusername/athena.git
cd athena
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
git clone https://github.com/yourusername/athena.git
cd athena
setup.bat
```

#### Option 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/athena.git
cd athena

# 2. Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install optional features (recommended)
pip install -r requirements_optional.txt

# 5. Verify installation
python check_setup.py
```

### Running Athena

```bash
# Make sure Ollama is running
ollama serve

# Start Athena
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 📖 Documentation

### Quick Start Guides
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [First Steps](docs/QUICKSTART.md) - Your first analysis
- [Feature Overview](docs/FEATURES.md) - Complete feature documentation

### Advanced Topics
- [Knowledge Graphs](docs/KNOWLEDGE_GRAPH_GUIDE.md) - Entity extraction and visualization
- [Multi-Document RAG](docs/ADVANCED_RAG_GUIDE.md) - Cross-paper reasoning
- [Voice Interface](docs/VOICE_INTERFACE_GUIDE.md) - Speech interaction
- [API Documentation](docs/API.md) - Programmatic usage

### Troubleshooting
- [Common Issues](docs/TROUBLESHOOTING.md) - Solutions to frequent problems
- [Performance Tuning](docs/PERFORMANCE.md) - Optimization tips
- [FAQ](docs/FAQ.md) - Frequently asked questions

---

## 🎯 Usage Examples

### 1. Analyze a Research Paper

```bash
# Start Athena
streamlit run app.py

# In the web interface:
# 1. Upload your PDF
# 2. Click "✨ Research"
# 3. Explore different tabs:
#    - Summary: High-level overview
#    - Q&A: Ask specific questions
#    - Search: Find relevant sections
#    - Chat: Conversational exploration
```

### 2. Build Knowledge Graph

```python
# In Athena web interface:
# 1. Upload research paper
# 2. Go to "🕸️ Knowledge Graph" tab
# 3. Click "Build Knowledge Graph"
# 4. Explore:
#    - Interactive visualization
#    - Entity queries
#    - Path finding
#    - Export options
```

### 3. Compare Multiple Papers

```python
# In Athena web interface:
# 1. Go to "📚 Advanced RAG" tab
# 2. Upload Paper 1 → "Add to RAG"
# 3. Upload Paper 2 → "Add to RAG"
# 4. Use comparison features:
#    - Ask cross-paper questions
#    - Compare methodologies
#    - Track concepts across papers
```

### 4. Voice Interaction (Optional)

```python
# Prerequisites:
# pip install openai-whisper gtts

# In Athena web interface:
# 1. Go to "🎤 Voice Assistant" tab
# 2. Record your question
# 3. Get spoken response
# 4. View transcription and answer
```

---

## 🗂️ Project Structure

```
athena/
├── app.py                          # Main Streamlit application
├── main.py                         # Research engine (online/offline)
├── qa_engine.py                    # Q&A system with FAISS
├── semantic_search.py              # Semantic search engine
├── chat_engine.py                  # Conversational AI
├── pdf_utils.py                    # PDF extraction utilities
│
├── advanced_rag.py                 # Multi-document RAG system
├── knowledge_graph.py              # Knowledge graph construction
├── kg_visualizer.py               # Graph visualization
├── document_comparison.py          # Document comparison engine
│
├── voice_engine.py                 # Voice processing (optional)
├── voice_interface.py             # Voice UI integration (optional)
│
├── tools/
│   ├── arxiv_search.py            # Arxiv paper search
│   └── web_search.py              # DuckDuckGo web search
│
├── docs/                           # Documentation
│   ├── INSTALLATION.md
│   ├── QUICKSTART.md
│   ├── FEATURES.md
│   ├── KNOWLEDGE_GRAPH_GUIDE.md
│   ├── ADVANCED_RAG_GUIDE.md
│   ├── VOICE_INTERFACE_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── API.md
│
├── tests/                          # Test scripts
│   ├── test_system.py             # Core system tests
│   ├── test_kg_rag_system.py     # KG + RAG tests
│   ├── test_comparison.py         # Document comparison tests
│   └── test_voice.py              # Voice interface tests
│
├── requirements.txt                # Core dependencies
├── requirements_optional.txt       # Optional features
├── setup.sh                        # Linux/macOS setup
├── setup.bat                       # Windows setup
├── check_setup.py                  # Installation verifier
│
└── README.md                       # This file
```

---

## ⚙️ Configuration

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB+ |
| Storage | 5 GB | 10 GB+ |
| CPU | 4 cores | 8+ cores |
| GPU | Not required | NVIDIA GPU (optional, for faster processing) |

### Ollama Models

**Default:** `llama3` (7B parameters)

**Alternatives:**
```bash
# Smaller (faster, less accurate)
ollama pull llama2:7b

# Larger (slower, more accurate)
ollama pull llama3:70b

# Specialized
ollama pull mistral
ollama pull codellama
```

### Performance Tuning

**For faster processing:**
```python
# In qa_engine.py, semantic_search.py
chunk_size = 1000  # Smaller = faster
k = 2              # Fewer results = faster
```

**For better quality:**
```python
# In qa_engine.py, semantic_search.py
chunk_size = 3000  # Larger = more context
k = 5              # More results = better coverage
temperature = 0.1  # Lower = more focused
```

---

## 🧪 Testing

### Run All Tests
```bash
# Core system test
python tests/test_system.py

# Knowledge Graph + RAG test
python tests/test_kg_rag_system.py

# Document comparison test
python tests/test_comparison.py

# Voice interface test (if installed)
python tests/test_voice.py
```

### Quick Verification
```bash
# Verify installation
python check_setup.py

# Check Ollama status
curl http://localhost:11434/api/tags
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/athena.git
cd athena

# 2. Create branch
git checkout -b feature/your-feature

# 3. Install dev dependencies
pip install -r requirements_dev.txt

# 4. Make changes and test
python -m pytest tests/

# 5. Submit pull request
```

### Areas for Contribution
- 🌐 Additional LLM providers (OpenAI, Anthropic)
- 🔍 OCR support for scanned PDFs
- 🌍 Multi-language support
- 📊 Enhanced visualizations
- 🧪 Additional test coverage

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with these amazing open-source projects:

- [Ollama](https://ollama.ai) - Local LLM runtime
- [LangChain](https://langchain.com) - LLM framework
- [Streamlit](https://streamlit.io) - Web framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search
- [Sentence Transformers](https://www.sbert.net/) - Embeddings
- [NetworkX](https://networkx.org/) - Graph analysis
- [Plotly](https://plotly.com/) - Interactive visualizations

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/athena/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/athena/discussions)
- **Email:** your.email@example.com

---

## 🗺️ Roadmap

### v2.0 (Coming Soon)
- [ ] Neo4j integration for large knowledge graphs
- [ ] LangGraph multi-agent workflows
- [ ] Enhanced document comparison
- [ ] Cloud deployment options
- [ ] API server mode

### v2.1 (Planned)
- [ ] Graph neural networks for similarity
- [ ] Temporal concept tracking
- [ ] Citation network analysis
- [ ] Collaborative features

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/athena?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/athena?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/athena)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/athena)

---

**Built with ❤️ for researchers and students**

*Making research accessible, one paper at a time* 🚀

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/athena&type=Date)](https://star-history.com/#yourusername/athena&Date)