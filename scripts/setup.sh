#!/bin/bash
# setup.sh - Automated Athena Setup for Linux/macOS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "============================================================"
echo "🧠 ATHENA - AI Research Assistant Setup"
echo "============================================================"
echo ""

# Check Python version
echo "1️⃣ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "Install Python 3.8+: https://www.python.org/downloads/"
    exit 1
fi

python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python $python_version${NC}"

# Check Python version >= 3.8
major=$(echo "$python_version" | cut -d. -f1)
minor=$(echo "$python_version" | cut -d. -f2)

if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 8 ]); then
    echo -e "${RED}❌ Python 3.8+ required (found $python_version)${NC}"
    exit 1
fi

echo ""

# Check Ollama
echo "2️⃣ Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo "Ollama is required for Athena to work."
    echo ""
    echo "Install from: https://ollama.ai"
    echo ""
    read -p "Continue without Ollama? (you'll need to install it later) [y/N]: " continue_setup
    if [[ ! $continue_setup =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ Ollama installed${NC}"
    
    # Check if Ollama is running
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama is running${NC}"
        
        # Check for llama3 model
        if ollama list | grep -q "llama3"; then
            echo -e "${GREEN}✅ llama3 model available${NC}"
        else
            echo -e "${YELLOW}⚠️  llama3 model not found${NC}"
            read -p "Download llama3 model now? (~4GB) [y/N]: " download_model
            if [[ $download_model =~ ^[Yy]$ ]]; then
                echo "Downloading llama3..."
                ollama pull llama3
            fi
        fi
    else
        echo -e "${YELLOW}⚠️  Ollama not running${NC}"
        echo "Start with: ollama serve"
    fi
fi

echo ""

# Create virtual environment
echo "3️⃣ Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    read -p "Recreate? [y/N]: " recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

echo -e "${GREEN}✅ Virtual environment ready${NC}"
echo ""

# Activate virtual environment
echo "4️⃣ Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✅ Activated${NC}"
echo ""

# Upgrade pip
echo "5️⃣ Upgrading pip..."
pip install --quiet --upgrade pip
echo -e "${GREEN}✅ pip upgraded${NC}"
echo ""

# Install core dependencies
echo "6️⃣ Installing core dependencies..."
echo "This may take 3-5 minutes..."
echo ""

if pip install -r requirements.txt; then
    echo -e "${GREEN}✅ Core dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""

# Install optional dependencies
echo "7️⃣ Installing optional features..."
read -p "Install optional features? (voice, advanced viz) [Y/n]: " install_optional

if [[ ! $install_optional =~ ^[Nn]$ ]]; then
    if [ -f "requirements_optional.txt" ]; then
        pip install -r requirements_optional.txt
        echo -e "${GREEN}✅ Optional features installed${NC}"
    else
        echo -e "${YELLOW}⚠️  requirements_optional.txt not found${NC}"
    fi
else
    echo "Skipping optional features"
fi

echo ""

# Run verification
echo "8️⃣ Verifying installation..."
if python check_setup.py; then
    echo -e "${GREEN}✅ Verification passed${NC}"
else
    echo -e "${YELLOW}⚠️  Some checks failed (see above)${NC}"
fi

echo ""

# Create .env file if needed
if [ ! -f ".env" ]; then
    echo "9️⃣ Creating configuration file..."
    cat > .env << EOF
# Athena Configuration
OLLAMA_URL=http://localhost:11434
MODEL_NAME=llama3
CHUNK_SIZE=2000
CHUNK_OVERLAP=200
EOF
    echo -e "${GREEN}✅ .env created${NC}"
fi

echo ""

# Summary
echo "============================================================"
echo "📊 SETUP COMPLETE"
echo "============================================================"
echo ""
echo -e "${GREEN}✅ Installation successful!${NC}"
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Start Ollama (if not running):"
echo "   ${BLUE}ollama serve${NC}"
echo ""
echo "2. Activate virtual environment:"
echo "   ${BLUE}source venv/bin/activate${NC}"
echo ""
echo "3. Start Athena:"
echo "   ${BLUE}streamlit run app.py${NC}"
echo ""
echo "4. Access in browser:"
echo "   ${BLUE}http://localhost:8501${NC}"
echo ""
echo "============================================================"
echo ""
echo "📚 Documentation: docs/"
echo "🐛 Issues: https://github.com/yourusername/athena/issues"
echo "💬 Discussions: https://github.com/yourusername/athena/discussions"
echo ""
echo "⭐ If you find Athena helpful, star us on GitHub!"
echo "============================================================"