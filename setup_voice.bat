@echo off
REM setup_voice.bat - Windows voice interface setup for Athena

echo ============================================================
echo 🎤 ATHENA VOICE INTERFACE SETUP (Windows)
echo ============================================================
echo.

REM Check Python
echo 1️⃣ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ Python not found! Please install Python 3.8+
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    Found: Python %PYTHON_VERSION%
echo    ✅ Python is installed
echo.

REM Install dependencies
echo 2️⃣ Installing voice dependencies...
echo    This may take 5-10 minutes...
echo.

pip install --upgrade openai-whisper gtts soundfile numpy
if errorlevel 1 (
    echo    ❌ Installation failed!
    pause
    exit /b 1
)

echo    ✅ Dependencies installed
echo.

REM Test Whisper
echo 3️⃣ Testing Whisper (Speech-to-Text)...
python -c "import whisper; model = whisper.load_model('base'); print('   ✅ Whisper loaded successfully!')"
if errorlevel 1 (
    echo    ❌ Whisper test failed
    pause
    exit /b 1
)
echo.

REM Test gTTS
echo 4️⃣ Testing gTTS (Text-to-Speech)...
python -c "from gtts import gTTS; import tempfile; tts = gTTS('Test', lang='en'); t = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3'); tts.save(t.name); t.close(); print('   ✅ gTTS working!')"
if errorlevel 1 (
    echo    ⚠️ gTTS test failed (check internet connection)
)
echo.

REM Test voice engine
echo 5️⃣ Testing Athena Voice Engine...
if exist voice_engine.py (
    python voice_engine.py
    if errorlevel 1 (
        echo    ⚠️ Voice engine test had issues
    ) else (
        echo    ✅ Voice engine test passed!
    )
) else (
    echo    ⚠️ voice_engine.py not found
)
echo.

REM Summary
echo ============================================================
echo 📊 SETUP SUMMARY
echo ============================================================
echo.
echo ✅ Python %PYTHON_VERSION%
echo ✅ Whisper (Speech-to-Text) - Offline
echo ✅ gTTS (Text-to-Speech) - Online
echo.
echo 🎯 Next Steps:
echo    1. Start Athena: streamlit run app.py
echo    2. Upload a document
echo    3. Go to '🎤 Voice Assistant' tab
echo    4. Start speaking!
echo.
echo 💡 Tips:
echo    - Use headphones to prevent feedback
echo    - Speak clearly at normal pace
echo    - First transcription may be slower (model loading)
echo.
echo 📚 Documentation:
echo    - Full guide: VOICE_INTERFACE_GUIDE.md
echo    - Test script: python voice_engine.py
echo.
echo ============================================================
echo 🎉 Setup complete! Happy voice researching!
echo ============================================================
echo.

pause