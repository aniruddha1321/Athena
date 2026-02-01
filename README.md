# Athena - AI Research Assistant

A powerful local AI-powered research assistant for analyzing academic papers, generating summaries, and answering questions.

## Project Structure

```
Athena/
├── app.py                      # Main Streamlit application
├── LICENSE                     # MIT License
│
├── src/                        # Core source code modules
│   ├── __init__.py
│   ├── advanced_rag.py         # Multi-document RAG implementation
│   ├── arxiv_search.py         # ArXiv paper search functionality
│   ├── chat_engine.py          # Conversational AI interface
│   ├── document_comparison.py  # Document comparison module
│   ├── kg_visualizer.py        # Knowledge graph visualization
│   ├── knowledge_graph.py      # Knowledge graph construction
│   ├── paper_fetcher.py        # Research paper fetching
│   ├── pdf_utils.py            # PDF processing utilities
│   ├── qa_engine.py            # Question-answering system
│   ├── semantic_search.py      # Semantic search implementation
│   ├── voice_engine.py         # Voice processing
│   ├── voice_interface.py      # Voice UI
│   └── web_search.py           # Web search functionality
│
├── tests/                      # Test files and debugging scripts
│   ├── check_setup.py
│   ├── debug_semantic_search.py
│   ├── demo_research.py
│   ├── ollama_debug.py
│   ├── test_comparison.py
│   ├── test_kg_rag_system.py
│   ├── test_pdf_cleaning.py
│   ├── test_system.py
│   └── test_voice.py
│
├── docs/                       # Documentation
│   ├── README.md               # Main documentation
│   ├── CHANGELOG.md            # Version history
│   ├── installation.md         # Installation guide
│   ├── RESEARCH_DOCUMENTATION.md  # Academic paper
│   ├── bug_report.md           # Bug report template
│   └── feature_request.md      # Feature request template
│
├── config/                     # Configuration files
│   ├── DockerFile              # Docker configuration
│   ├── docker-compose.yml      # Docker Compose setup
│   ├── .dockerignore
│   ├── requirements.txt        # Python dependencies
│   └── requirements_kg_rag.txt # Optional KG/RAG dependencies
│
├── scripts/                    # Setup and utility scripts
│   ├── setup.bat               # Windows setup
│   ├── setup.sh                # Linux/Mac setup
│   ├── setup_kg_rag.bat        # KG/RAG setup (Windows)
│   ├── setup_kg_rag.sh         # KG/RAG setup (Linux/Mac)
│   ├── setup_voice.bat         # Voice setup (Windows)
│   ├── setup_voice.sh          # Voice setup (Linux/Mac)
│   └── MakeFile                # Make commands
│
├── assets/                     # Static assets
│   ├── athena.png              # Application logo
│   ├── knowledge_graph.html    # KG visualization template
│   └── test_*.mp3/wav          # Test audio files
│
└── .github/                    # GitHub configurations
    ├── ci.yml                  # CI/CD workflow
    ├── release.yml             # Release workflow
    ├── pre-commit-config.yaml
    └── pull-request-template.md
```

## Quick Start

### Installation

1. **Install dependencies:**
   ```bash
   # Windows
   scripts\setup.bat
   
   # Linux/Mac
   bash scripts/setup.sh
   ```

2. **Install Ollama and pull model:**
   ```bash
   # Download from: https://ollama.ai/
   ollama pull llama3.2:1b
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Optional Features

**Knowledge Graphs & Advanced RAG:**
```bash
# Windows
scripts\setup_kg_rag.bat

# Linux/Mac
bash scripts/setup_kg_rag.sh
```

**Voice Interface:**
```bash
# Windows
scripts\setup_voice.bat

# Linux/Mac
bash scripts/setup_voice.sh
```

## Features

- **Research & Summarize** - Upload PDFs or search topics for AI-generated summaries
- **Smart Q&A** - Ask questions about your documents with context-aware answers
- **Semantic Search** - Find concepts using AI-powered understanding
- **Chat Interface** - Natural conversations about research topics
- **Knowledge Graphs** - Visualize relationships between concepts (optional)
- **Advanced RAG** - Query across multiple documents (optional)
- **Document Comparison** - Compare papers side-by-side (optional)
- **Voice Interface** - Voice-enabled interaction (optional)

## Requirements

- Python 3.9+
- 8GB RAM (minimum)
- Ollama installed and running
- 5GB free disk space

## License

MIT License - see LICENSE file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
---