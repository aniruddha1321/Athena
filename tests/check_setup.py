#!/usr/bin/env python3
"""
check_setup.py - Comprehensive Athena Installation Verifier

This script checks:
- Python version
- Core dependencies
- Optional dependencies
- Ollama connection
- File system setup
- Configuration files

Run: python check_setup.py
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 70}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")


def check_python_version() -> bool:
    """Check if Python version is 3.8+"""
    print_header("1️⃣  Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"   Python version: {version_str}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} meets requirements (3.8+)")
        return True
    else:
        print_error(f"Python {version_str} is too old. Need 3.8+")
        print_info("Download from: https://www.python.org/downloads/")
        return False


def check_core_dependencies() -> Tuple[bool, List[str]]:
    """Check core package installation"""
    print_header("2️⃣  Core Dependencies Check")
    
    core_packages = {
        'streamlit': 'streamlit',
        'PyPDF2': 'PyPDF2',
        'langchain': 'langchain',
        'langchain_community': 'langchain-community',
        'faiss': 'faiss-cpu',
        'sentence_transformers': 'sentence-transformers',
        'requests': 'requests',
        'duckduckgo_search': 'duckduckgo-search',
        'arxiv': 'arxiv',
    }
    
    missing = []
    installed = []
    
    for module, package in core_packages.items():
        try:
            __import__(module)
            print_success(package)
            installed.append(package)
        except ImportError:
            print_error(f"{package} - Install: pip install {package}")
            missing.append(package)
    
    print(f"\n   Installed: {len(installed)}/{len(core_packages)}")
    
    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        print_info("Install with: pip install -r requirements.txt")
        return False, missing
    
    print_success("All core dependencies installed!")
    return True, []


def check_optional_dependencies() -> Dict[str, bool]:
    """Check optional feature availability"""
    print_header("3️⃣  Optional Features Check")
    
    features = {}
    
    # Knowledge Graph + RAG
    try:
        import networkx
        import plotly
        import sklearn
        print_success("Knowledge Graph + RAG: Available")
        features['kg_rag'] = True
    except ImportError as e:
        print_warning(f"Knowledge Graph + RAG: Missing ({e.name})")
        print_info("Install: pip install networkx plotly scikit-learn")
        features['kg_rag'] = False
    
    # PyVis (enhanced visualization)
    try:
        import pyvis
        print_success("PyVis (enhanced viz): Available")
        features['pyvis'] = True
    except ImportError:
        print_warning("PyVis: Not installed (optional)")
        print_info("Install: pip install pyvis")
        features['pyvis'] = False
    
    # Voice Interface
    try:
        import whisper
        import gtts
        print_success("Voice Interface: Available")
        features['voice'] = True
    except ImportError as e:
        print_warning(f"Voice Interface: Missing ({e.name if hasattr(e, 'name') else 'dependencies'})")
        print_info("Install: pip install openai-whisper gtts")
        features['voice'] = False
    
    return features


def check_ollama() -> Tuple[bool, str]:
    """Check Ollama installation and status"""
    print_header("4️⃣  Ollama Check")
    
    # Check if ollama command exists
    try:
        result = subprocess.run(
            ['ollama', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"Ollama installed: {version}")
        else:
            print_warning("Ollama command found but version check failed")
    except FileNotFoundError:
        print_error("Ollama not found in PATH")
        print_info("Install from: https://ollama.ai")
        return False, "not_installed"
    except Exception as e:
        print_warning(f"Could not verify Ollama: {e}")
    
    # Check if Ollama is running
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        
        if response.status_code == 200:
            print_success("Ollama server is running")
            
            # Check for models
            models = response.json().get('models', [])
            
            if models:
                print(f"\n   Available models:")
                for model in models:
                    model_name = model.get('name', 'unknown')
                    size = model.get('size', 0) / (1024**3)  # Convert to GB
                    print(f"   • {model_name} ({size:.1f} GB)")
                
                # Check for llama3
                has_llama3 = any('llama3' in m.get('name', '') for m in models)
                
                if has_llama3:
                    print_success("llama3 model available (recommended)")
                    return True, "running_with_model"
                else:
                    print_warning("llama3 model not found")
                    print_info("Install: ollama pull llama3")
                    return True, "running_no_model"
            else:
                print_warning("No models installed")
                print_info("Install: ollama pull llama3")
                return True, "running_no_model"
        else:
            print_error(f"Ollama server error: {response.status_code}")
            return False, "error"
            
    except requests.exceptions.ConnectionError:
        print_error("Ollama server not running")
        print_info("Start with: ollama serve")
        return False, "not_running"
    except Exception as e:
        print_warning(f"Could not connect to Ollama: {e}")
        return False, "error"


def check_project_structure() -> bool:
    """Check if required files exist"""
    print_header("5️⃣  Project Structure Check")
    
    required_files = [
        'app.py',
        'main.py',
        'qa_engine.py',
        'semantic_search.py',
        'chat_engine.py',
        'pdf_utils.py',
        'requirements.txt',
    ]
    
    optional_files = [
        'knowledge_graph.py',
        'advanced_rag.py',
        'kg_visualizer.py',
        'document_comparison.py',
        'voice_engine.py',
        'voice_interface.py',
    ]
    
    all_present = True
    
    print("   Core files:")
    for file in required_files:
        if Path(file).exists():
            print_success(file)
        else:
            print_error(f"{file} - MISSING!")
            all_present = False
    
    print("\n   Optional files:")
    for file in optional_files:
        if Path(file).exists():
            print_success(file)
        else:
            print_info(f"{file} - Not present (optional)")
    
    # Check tools directory
    if Path('tools').is_dir():
        print_success("tools/ directory")
    else:
        print_warning("tools/ directory missing")
    
    return all_present


def check_configuration() -> bool:
    """Check configuration files"""
    print_header("6️⃣  Configuration Check")
    
    # Check for .env or .env.example
    has_env = Path('.env').exists()
    has_env_example = Path('.env.example').exists()
    
    if has_env:
        print_success(".env file present")
    elif has_env_example:
        print_warning(".env not found (using .env.example)")
        print_info("Copy .env.example to .env and configure")
    else:
        print_warning("No configuration file found")
        print_info("This is optional, but recommended")
    
    # Check .gitignore
    if Path('.gitignore').exists():
        print_success(".gitignore present")
    else:
        print_warning(".gitignore missing (recommended)")
    
    return True


def run_quick_test() -> bool:
    """Run quick functionality test"""
    print_header("7️⃣  Quick Functionality Test")
    
    try:
        # Test embeddings
        print("   Testing embeddings...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(["Test sentence"])
        print_success(f"Embeddings working (dim: {len(embeddings[0])})")
        
        # Test FAISS
        print("   Testing FAISS...")
        from langchain_community.vectorstores import FAISS
        from langchain_community.embeddings import SentenceTransformerEmbeddings
        
        embed = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        texts = ["Test 1", "Test 2"]
        vectordb = FAISS.from_texts(texts, embed)
        print_success("FAISS working")
        
        print_success("Quick tests passed!")
        return True
        
    except Exception as e:
        print_error(f"Quick test failed: {e}")
        return False


def generate_report(results: Dict) -> str:
    """Generate summary report"""
    print_header("📊 SUMMARY REPORT")
    
    score = 0
    max_score = 7
    
    # Python version
    if results['python_ok']:
        score += 1
        print_success("Python version")
    else:
        print_error("Python version")
    
    # Core dependencies
    if results['core_ok']:
        score += 1
        print_success("Core dependencies")
    else:
        print_error("Core dependencies")
    
    # Optional features
    optional_count = sum(results['features'].values())
    if optional_count > 0:
        print_info(f"Optional features: {optional_count}/3")
    
    # Ollama
    ollama_status = results['ollama_status']
    if ollama_status == 'running_with_model':
        score += 1
        print_success("Ollama + model")
    elif ollama_status == 'running_no_model':
        print_warning("Ollama running (no model)")
    else:
        print_error("Ollama")
    
    # Project structure
    if results['structure_ok']:
        score += 1
        print_success("Project structure")
    else:
        print_error("Project structure")
    
    # Quick test
    if results.get('test_ok'):
        score += 1
        print_success("Functionality test")
    else:
        print_warning("Functionality test")
    
    # Overall status
    print(f"\n   Overall Score: {score}/{max_score}")
    
    if score >= 5:
        print_success("System ready to use! 🎉")
        status = "ready"
    elif score >= 3:
        print_warning("System partially ready (some issues)")
        status = "partial"
    else:
        print_error("System not ready (critical issues)")
        status = "not_ready"
    
    return status


def print_next_steps(status: str, results: Dict):
    """Print recommended next steps"""
    print_header("🎯 NEXT STEPS")
    
    if status == "ready":
        print("   You're all set! To start Athena:\n")
        print(f"   {Colors.BLUE}1. Start Ollama:{Colors.RESET}")
        print("      ollama serve\n")
        print(f"   {Colors.BLUE}2. Start Athena:{Colors.RESET}")
        print("      streamlit run app.py\n")
        print(f"   {Colors.BLUE}3. Open in browser:{Colors.RESET}")
        print("      http://localhost:8501\n")
        
    elif status == "partial":
        print("   Fix these issues:\n")
        
        if not results['python_ok']:
            print("   • Upgrade Python to 3.8+")
        
        if not results['core_ok']:
            print("   • Install missing dependencies:")
            print("     pip install -r requirements.txt")
        
        if results['ollama_status'] == 'not_running':
            print("   • Start Ollama:")
            print("     ollama serve")
        
        if results['ollama_status'] == 'running_no_model':
            print("   • Install llama3 model:")
            print("     ollama pull llama3")
        
        print("\n   Then run: python check_setup.py")
        
    else:
        print("   Critical issues found:\n")
        
        if not results['python_ok']:
            print("   • Install Python 3.8+")
            print("     https://www.python.org/downloads/")
        
        if not results['core_ok']:
            print("   • Install core dependencies:")
            print("     pip install -r requirements.txt")
        
        if not results['structure_ok']:
            print("   • Ensure all project files are present")
            print("     Re-clone repository or check download")
        
        print("\n   After fixing, run: python check_setup.py")
    
    print(f"\n   {Colors.BLUE}📚 Documentation:{Colors.RESET} docs/")
    print(f"   {Colors.BLUE}🐛 Report issues:{Colors.RESET} GitHub Issues")
    print(f"   {Colors.BLUE}💬 Get help:{Colors.RESET} GitHub Discussions\n")


def main():
    """Main verification routine"""
    print_header("🧠 ATHENA INSTALLATION VERIFIER")
    
    results = {}
    
    # Run checks
    results['python_ok'] = check_python_version()
    results['core_ok'], results['missing_packages'] = check_core_dependencies()
    results['features'] = check_optional_dependencies()
    results['ollama_ok'], results['ollama_status'] = check_ollama()
    results['structure_ok'] = check_project_structure()
    results['config_ok'] = check_configuration()
    
    # Run quick test only if core is OK
    if results['core_ok']:
        results['test_ok'] = run_quick_test()
    else:
        results['test_ok'] = False
    
    # Generate report
    status = generate_report(results)
    
    # Next steps
    print_next_steps(status, results)
    
    # Exit code
    if status == "ready":
        return 0
    elif status == "partial":
        return 1
    else:
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Check cancelled by user{Colors.RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)