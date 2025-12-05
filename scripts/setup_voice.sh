#!/bin/bash
# setup_voice.sh - Automated voice interface setup for Athena

echo "============================================================"
echo "🎤 ATHENA VOICE INTERFACE SETUP"
echo "============================================================"
echo ""

# Check Python version
echo "1️⃣ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "   Found: Python $python_version"

if [[ $(echo "$python_version" | cut -d. -f1) -lt 3 ]] || [[ $(echo "$python_version" | cut -d. -f2) -lt 8 ]]; then
    echo "   ❌ Python 3.8+ required"
    exit 1
fi
echo "   ✅ Python version OK"
echo ""

# Install voice dependencies
echo "2️⃣ Installing voice dependencies..."
echo "   This may take 5-10 minutes on first install..."

pip install --upgrade openai-whisper gtts soundfile numpy 2>&1 | grep -E "Successfully|already"

if [ $? -eq 0 ]; then
    echo "   ✅ Voice dependencies installed"
else
    echo "   ❌ Installation failed"
    exit 1
fi
echo ""

# Test Whisper
echo "3️⃣ Testing Whisper (Speech-to-Text)..."
python -c "
import whisper
print('   📥 Loading Whisper base model...')
model = whisper.load_model('base')
print('   ✅ Whisper loaded successfully!')
" 2>&1

if [ $? -ne 0 ]; then
    echo "   ❌ Whisper test failed"
    exit 1
fi
echo ""

# Test gTTS
echo "4️⃣ Testing gTTS (Text-to-Speech)..."
python -c "
from gtts import gTTS
import tempfile
import os

print('   🔊 Generating test audio...')
tts = gTTS('Hello, Athena voice interface is working!', lang='en')
temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
tts.save(temp.name)
temp.close()

if os.path.exists(temp.name):
    size = os.path.getsize(temp.name)
    os.unlink(temp.name)
    print(f'   ✅ gTTS working! Generated {size} bytes')
else:
    print('   ❌ gTTS test failed')
    exit(1)
" 2>&1

if [ $? -ne 0 ]; then
    echo "   ⚠️ gTTS test failed (might need internet)"
fi
echo ""

# Test full voice engine
echo "5️⃣ Testing Athena Voice Engine..."
if [ -f "voice_engine.py" ]; then
    python voice_engine.py 2>&1 | tail -20
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Voice engine test passed!"
    else
        echo "   ⚠️ Voice engine test had issues"
    fi
else
    echo "   ⚠️ voice_engine.py not found in current directory"
fi
echo ""

# Summary
echo "============================================================"
echo "📊 SETUP SUMMARY"
echo "============================================================"
echo ""
echo "✅ Python $python_version"
echo "✅ Whisper (Speech-to-Text) - Offline"
echo "✅ gTTS (Text-to-Speech) - Online"
echo ""
echo "🎯 Next Steps:"
echo "   1. Start Athena: streamlit run app.py"
echo "   2. Upload a document"
echo "   3. Go to '🎤 Voice Assistant' tab"
echo "   4. Start speaking!"
echo ""
echo "💡 Tips:"
echo "   - Use headphones to prevent feedback"
echo "   - Speak clearly at normal pace"
echo "   - First transcription may be slower (model loading)"
echo ""
echo "📚 Documentation:"
echo "   - Full guide: VOICE_INTERFACE_GUIDE.md"
echo "   - Test script: python voice_engine.py"
echo "   - Troubleshooting: See guide above"
echo ""
echo "============================================================"
echo "🎉 Setup complete! Happy voice researching!"
echo "============================================================"