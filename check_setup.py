#!/usr/bin/env python3
"""
Check which Athena features are available
"""

import os
import sys

print("=" * 70)
print("🔍 ATHENA SETUP CHECKER")
print("=" * 70)
print()

# Core files
core_files = {
    'app.py': 'Main application',
    'main.py': 'Research engine',
    'qa_engine.py': 'Q&A system',
    'semantic_search.py': 'Semantic search',
    'pdf_utils.py': 'PDF utilities',
    'chat_engine.py': 'Chat interface'
}

# Optional files
optional_files = {
    'document_comparison.py': 'Document comparison feature',
    'voice_engine.py': 'Voice processing',
    'voice_interface.py': 'Voice UI integration'
}

print("📁 CORE FILES:")
print("-" * 70)
all_core_present = True
for file, desc in core_files.items():
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"{status} {file:30s} - {desc}")
    if not exists:
        all_core_present = False

print()
print("🎁 OPTIONAL FEATURES:")
print("-" * 70)
comparison_available = os.path.exists('document_comparison.py')
voice_engine_available = os.path.exists('voice_engine.py')
voice_interface_available = os.path.exists('voice_interface.py')

print(f"{'✅' if comparison_available else '❌'} document_comparison.py    - Document comparison feature")
print(f"{'✅' if voice_engine_available else '❌'} voice_engine.py          - Voice processing")
print(f"{'✅' if voice_interface_available else '❌'} voice_interface.py       - Voice UI integration")

print()
print("📦 PYTHON PACKAGES:")
print("-" * 70)

required_packages = [
    ('streamlit', 'Core framework'),
    ('langchain', 'LLM framework'),
    ('faiss', 'Vector search (faiss-cpu)'),
    ('sentence_transformers', 'Embeddings'),
]

optional_packages = [
    ('sklearn', 'ML utilities (scikit-learn)', comparison_available),
    ('whisper', 'Speech-to-Text (openai-whisper)', voice_engine_available),
    ('gtts', 'Text-to-Speech', voice_engine_available),
]

packages_ok = True
for package, desc in required_packages:
    try:
        __import__(package)
        print(f"✅ {package:25s} - {desc}")
    except ImportError:
        print(f"❌ {package:25s} - {desc} (MISSING)")
        packages_ok = False

print()
print("Optional packages:")
for package, desc, needed in optional_packages:
    if needed:
        try:
            __import__(package)
            print(f"✅ {package:25s} - {desc}")
        except ImportError:
            print(f"⚠️  {package:25s} - {desc} (needed but missing)")
    else:
        print(f"⏭️  {package:25s} - {desc} (not needed)")

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)

# Core status
if all_core_present and packages_ok:
    print("✅ Core features: READY")
else:
    print("❌ Core features: INCOMPLETE")
    if not all_core_present:
        print("   Missing core files - check above")
    if not packages_ok:
        print("   Missing packages - run: pip install -r requirements.txt")

# Optional features status
features = []
if comparison_available:
    if os.path.exists('sklearn'):
        features.append("✅ Document Comparison")
    else:
        print("⚠️  Document Comparison: File present but missing scikit-learn")
        print("   Install: pip install scikit-learn")
else:
    print("ℹ️  Document Comparison: Not installed")

if voice_engine_available and voice_interface_available:
    try:
        import whisper
        import gtts
        features.append("✅ Voice Assistant")
    except ImportError as e:
        print(f"⚠️  Voice Assistant: Files present but missing: {e.name}")
        print("   Install: pip install openai-whisper gtts soundfile")
elif voice_engine_available:
    print("⚠️  Voice Assistant: voice_interface.py missing")
    print("   Create this file from the artifact")
else:
    print("ℹ️  Voice Assistant: Not installed")

if features:
    print()
    print("🎉 Available optional features:")
    for f in features:
        print(f"   {f}")

print()
print("=" * 70)
print("🚀 NEXT STEPS")
print("=" * 70)

if not all_core_present:
    print("1. ❌ Fix missing core files first!")
    print("   - Download missing files from GitHub")
elif not packages_ok:
    print("1. ❌ Install missing packages:")
    print("   pip install -r requirements.txt")
else:
    print("✅ Core system ready!")
    print()
    print("To start Athena:")
    print("   streamlit run app.py")
    print()
    
    if not comparison_available:
        print("To add Document Comparison:")
        print("   1. Create document_comparison.py (from artifact)")
        print("   2. pip install scikit-learn")
        print()
    
    if not (voice_engine_available and voice_interface_available):
        print("To add Voice Assistant:")
        if not voice_engine_available:
            print("   1. You already have voice_engine.py!")
        if not voice_interface_available:
            print("   1. Create voice_interface.py (from artifact)")
        print("   2. pip install openai-whisper gtts soundfile")
        print()

print("=" * 70)
print("📚 For help, see README.md or documentation files")
print("=" * 70)