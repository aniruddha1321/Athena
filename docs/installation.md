# INSTALLATION.md - Detailed Installation Guide

## 📋 Table of Contents
- [System Requirements](#system-requirements)
- [Quick Install](#quick-install)
- [Manual Installation](#manual-installation)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 8 GB
- **Storage**: 5 GB free space
- **Internet**: Required for initial setup and optional features

### Recommended Requirements
- **RAM**: 16 GB or more
- **Storage**: 10 GB free space
- **CPU**: 8+ cores for better performance
- **GPU**: NVIDIA GPU (optional, for faster processing)

---

## Quick Install

### Automated Setup (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/yourusername/athena.git
cd athena
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
git clone https://github.com/yourusername/athena.git
cd athena
setup.bat
```

The automated installer will:
1. ✅ Check Python version
2. ✅ Verify Ollama installation
3. ✅ Create virtual environment
4. ✅ Install all dependencies
5. ✅ Run verification tests
6. ✅ Configure environment

---

## Manual Installation

### Step 1: Install Prerequisites

#### Python 3.8+
**Check current version:**
```bash
python --version  # or python3 --version
```

**Install if needed:**
- **Windows**: [python.org/downloads](https://www.python.org/downloads/)
- **macOS**: `brew install python@3.10`
- **Linux**: `sudo apt install python3.10 python3-pip`

#### Ollama
**Install Ollama:**
1. Visit [ollama.ai](https://ollama.ai)
2. Download installer for your OS
3. Run installer
4. Verify: `ollama --version`

**Pull llama3 model:**
```bash
ollama pull llama3
```

**Start Ollama server:**
```bash
ollama serve
```

### Step 2: Clone Repository
```bash
git clone https://github.com/yourusername/athena.git
cd athena
```

### Step 3: Create Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 4: Install Dependencies

**Core dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Optional features:**
```bash
# Knowledge Graph + Advanced RAG
pip install networkx plotly pyvis scikit-learn

# Voice Interface
pip install openai-whisper gtts soundfile

# Or install all optional features
pip install -r requirements_optional.txt
```

### Step 5: Verify Installation
```bash
python check_setup.py
```

### Step 6: Configure (Optional)
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

### Step 7: Run Athena
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## Platform-Specific Instructions

### Windows

**Prerequisites:**
- Install [Python from python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation

**Common Issues:**
- If `pip` not found: Use `python -m pip` instead
- If script execution blocked: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- For voice features: Consider using `faster-whisper` instead of `openai-whisper`

**Voice Interface on Windows:**
```powershell
# Use faster-whisper (no FFmpeg needed)
pip uninstall openai-whisper
pip install faster-whisper
```

### macOS

**Prerequisites:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Install Ollama
brew install ollama
```

**Common Issues:**
- If SSL errors: `pip install --upgrade certifi`
- If `xcrun` errors: `xcode-select --install`

### Linux (Ubuntu/Debian)

**Prerequisites:**
```bash
# Update system
sudo apt update && sudo apt upgrade

# Install Python and tools
sudo apt install python3.10 python3-pip python3-venv

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

**Common Issues:**
- If `pip` not found: `sudo apt install python3-pip`
- If SSL errors: `sudo apt install ca-certificates`
- For GPU support: Install CUDA toolkit

---

## Verifying Installation

### Automated Verification
```bash
python check_setup.py
```

Expected output:
```
✅ Python version
✅ Core dependencies
✅ Ollama + model
✅ Project structure
✅ Functionality test
```

### Manual Verification

**1. Test Python:**
```bash
python -c "import sys; print(sys.version)"
```

**2. Test Dependencies:**
```bash
python -c "import streamlit, langchain, faiss"
```

**3. Test Ollama:**
```bash
curl http://localhost:11434/api/tags
```

**4. Test Athena:**
```bash
streamlit run app.py
```

---

## Troubleshooting

### Installation Fails

**Error: `pip install` fails**
```bash
# Try with --no-cache-dir
pip install --no-cache-dir -r requirements.txt

# Or upgrade pip first
pip install --upgrade pip setuptools wheel
```

**Error: Permission denied**
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Or install for user only
pip install --user -r requirements.txt
```

**Error: FAISS installation fails**
```bash
# Try CPU version explicitly
pip install faiss-cpu

# On ARM Mac (M1/M2)
conda install -c pytorch faiss-cpu
```

### Ollama Issues

**Ollama not starting:**
```bash
# Check if already running
ps aux | grep ollama  # Linux/macOS
tasklist | findstr ollama  # Windows

# Kill existing process
killall ollama  # Linux/macOS

# Start fresh
ollama serve
```

**Model download fails:**
```bash
# Check disk space
df -h  # Linux/macOS
dir    # Windows

# Try different mirror
OLLAMA_HOST=http://localhost:11434 ollama pull llama3
```

### Runtime Errors

**Error: "Could not connect to Ollama"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

**Error: "No module named 'X'"**
```bash
# Ensure virtual environment is activated
which python  # Should point to venv

# Reinstall package
pip install --force-reinstall <package-name>
```

**Error: Out of memory**
```bash
# Use smaller model
ollama pull llama2:7b

# Or reduce chunk sizes in config
# Edit app.py: chunk_size=1000
```

---

## Additional Resources

- **Documentation**: [docs/](docs/)
- **FAQ**: [docs/FAQ.md](docs/FAQ.md)
- **Troubleshooting Guide**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **GitHub Issues**: [github.com/yourusername/athena/issues](https://github.com/yourusername/athena/issues)
- **Community Discussions**: [github.com/yourusername/athena/discussions](https://github.com/yourusername/athena/discussions)

---

# CONTRIBUTING.md - Contribution Guidelines

## 🤝 Welcome Contributors!

Thank you for your interest in contributing to Athena! This guide will help you get started.

---

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Review Process](#review-process)

---

## Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards
- ✅ Be respectful and inclusive
- ✅ Accept constructive criticism gracefully
- ✅ Focus on what's best for the community
- ❌ No trolling, harassment, or discrimination

---

## Getting Started

### Ways to Contribute
1. **🐛 Report Bugs** - Found an issue? Let us know!
2. **💡 Suggest Features** - Have ideas? Share them!
3. **📝 Improve Documentation** - Help others understand
4. **🔧 Fix Issues** - Pick from open issues
5. **✨ Add Features** - Implement new capabilities

### Before You Start
1. Check [existing issues](https://github.com/yourusername/athena/issues)
2. Read [documentation](docs/)
3. Join our [discussions](https://github.com/yourusername/athena/discussions)

---

## Development Setup

### 1. Fork & Clone
```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/athena.git
cd athena
```

### 2. Create Branch
```bash
git checkout -b feature/your-feature-name
```

Branch naming:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 3. Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_dev.txt

# Install pre-commit hooks
pre-commit install
```

### 4. Verify Setup
```bash
python check_setup.py
pytest tests/
```

---

## Making Changes

### Development Workflow

1. **Make changes** in your branch
2. **Test thoroughly** (see Testing section)
3. **Update documentation** if needed
4. **Commit with clear messages**
5. **Push to your fork**
6. **Create pull request**

### Commit Message Format
```
type(scope): brief description

Detailed explanation of changes (if needed)

Fixes #issue_number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

**Examples:**
```bash
feat(rag): add multi-document comparison
fix(pdf): handle empty PDF files correctly
docs(readme): update installation instructions
```

---

## Coding Standards

### Python Style Guide
We follow [PEP 8](https://pep8.org/) with these tools:

**Black** (code formatting):
```bash
black app.py
```

**isort** (import sorting):
```bash
isort app.py
```

**flake8** (linting):
```bash
flake8 app.py
```

**Run all formatters:**
```bash
black . && isort . && flake8 .
```

### Code Quality Guidelines

**DO:**
- ✅ Write clear, self-documenting code
- ✅ Add docstrings to functions
- ✅ Handle errors gracefully
- ✅ Keep functions focused and small
- ✅ Use type hints where appropriate

**DON'T:**
- ❌ Leave commented-out code
- ❌ Use magic numbers
- ❌ Write functions > 50 lines
- ❌ Ignore linter warnings
- ❌ Skip error handling

### Documentation Standards

**Docstring format:**
```python
def process_document(text: str, chunk_size: int = 1000) -> List[str]:
    """
    Process document text into chunks.
    
    Args:
        text: Input text to process
        chunk_size: Maximum chunk size in characters
        
    Returns:
        List of text chunks
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> chunks = process_document("Long text...", 500)
        >>> len(chunks)
        5
    """
    pass
```

---

## Testing

### Running Tests

**All tests:**
```bash
pytest
```

**Specific test file:**
```bash
pytest tests/test_system.py
```

**With coverage:**
```bash
pytest --cov=. --cov-report=html
```

### Writing Tests

**Test structure:**
```python
# tests/test_feature.py

def test_function_success():
    """Test successful case"""
    result = my_function("input")
    assert result == "expected"


def test_function_error():
    """Test error handling"""
    with pytest.raises(ValueError):
        my_function(None)
```

**Test requirements:**
- ✅ Cover happy path
- ✅ Test edge cases
- ✅ Test error conditions
- ✅ Use descriptive names
- ✅ Keep tests independent

---

## Submitting Changes

### Pull Request Process

1. **Update your branch:**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Push changes:**
```bash
git push origin feature/your-feature-name
```

3. **Create PR on GitHub**

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear

## Screenshots (if applicable)

## Related Issues
Fixes #issue_number
```

### PR Best Practices
- ✅ Keep PRs focused and small
- ✅ Write clear descriptions
- ✅ Update documentation
- ✅ Respond to reviews promptly
- ✅ Be open to feedback

---

## Review Process

### What Reviewers Look For
1. **Code Quality** - Follows standards
2. **Testing** - Adequate coverage
3. **Documentation** - Clear and complete
4. **Functionality** - Works as intended
5. **No Breaking Changes** - Or properly documented

### Timeline
- Initial review: 2-3 days
- Follow-up reviews: 1-2 days
- Merge approval: After 2 approvals

### After Review
- Address feedback
- Push updates
- Request re-review
- Wait for approval

---

## Priority Areas for Contribution

### High Priority
- 🔴 **Bug Fixes** - Always welcome!
- 🟡 **Performance Improvements**
- 🟢 **Documentation Enhancements**

### Feature Requests
- 🌐 Additional LLM providers
- 🔍 OCR for scanned PDFs
- 🌍 Multi-language support
- 📊 Enhanced visualizations
- 🧪 More test coverage

### Good First Issues
Look for issues tagged `good-first-issue`

---

## Questions?

- **GitHub Discussions**: Ask questions
- **GitHub Issues**: Report bugs
- **Email**: your.email@example.com

---

## Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Acknowledged in documentation

---

**Thank you for contributing to Athena! 🎉**

Together, we're making research more accessible for everyone.