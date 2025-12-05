# ============================================================
# Windows Setup Script (setup.bat)
# ============================================================

# Save this as setup.bat for Windows users:

<</BAT
@echo off
REM setup.bat - Automated Athena Setup for Windows

echo ============================================================
echo 🧠 ATHENA - AI Research Assistant Setup
echo ============================================================
echo.

REM Check Python
echo 1️⃣ Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    echo Install Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%
echo.

REM Check Ollama
echo 2️⃣ Checking Ollama installation...
where ollama >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama not found
    echo.
    echo Ollama is required for Athena to work.
    echo Install from: https://ollama.ai
    echo.
    set /p continue_setup="Continue without Ollama? (you'll need to install it later) [y/N]: "
    if /i not "%continue_setup%"=="y" exit /b 1
) else (
    echo ✅ Ollama installed
    
    REM Check if Ollama is running
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Ollama is running
        
        REM Check for llama3 model
        ollama list | findstr "llama3" >nul 2>&1
        if not errorlevel 1 (
            echo ✅ llama3 model available
        ) else (
            echo ⚠️  llama3 model not found
            set /p download_model="Download llama3 model now? (~4GB) [y/N]: "
            if /i "%download_model%"=="y" (
                echo Downloading llama3...
                ollama pull llama3
            )
        )
    ) else (
        echo ⚠️  Ollama not running
        echo Start with: ollama serve
    )
)
echo.

REM Create virtual environment
echo 3️⃣ Creating virtual environment...
if exist venv (
    echo ⚠️  Virtual environment already exists
    set /p recreate="Recreate? [y/N]: "
    if /i "%recreate%"=="y" (
        rmdir /s /q venv
        python -m venv venv
    )
) else (
    python -m venv venv
)
echo ✅ Virtual environment ready
echo.

REM Activate virtual environment
echo 4️⃣ Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Activated
echo.

REM Upgrade pip
echo 5️⃣ Upgrading pip...
python -m pip install --quiet --upgrade pip
echo ✅ pip upgraded
echo.

REM Install core dependencies
echo 6️⃣ Installing core dependencies...
echo This may take 3-5 minutes...
echo.

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Core dependencies installed
echo.

REM Install optional dependencies
echo 7️⃣ Installing optional features...
set /p install_optional="Install optional features? (voice, advanced viz) [Y/n]: "

if /i not "%install_optional%"=="n" (
    if exist requirements_optional.txt (
        pip install -r requirements_optional.txt
        echo ✅ Optional features installed
    ) else (
        echo ⚠️  requirements_optional.txt not found
    )
) else (
    echo Skipping optional features
)
echo.

REM Run verification
echo 8️⃣ Verifying installation...
python check_setup.py
echo.

REM Create .env file if needed
if not exist .env (
    echo 9️⃣ Creating configuration file...
    (
        echo # Athena Configuration
        echo OLLAMA_URL=http://localhost:11434
        echo MODEL_NAME=llama3
        echo CHUNK_SIZE=2000
        echo CHUNK_OVERLAP=200
    ) > .env
    echo ✅ .env created
)
echo.

REM Summary
echo ============================================================
echo 📊 SETUP COMPLETE
echo ============================================================
echo.
echo ✅ Installation successful!
echo.
echo 🎯 Next Steps:
echo.
echo 1. Start Ollama (if not running):
echo    ollama serve
echo.
echo 2. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 3. Start Athena:
echo    streamlit run app.py
echo.
echo 4. Access in browser:
echo    http://localhost:8501
echo.
echo ============================================================
echo.
echo 📚 Documentation: docs\
echo 🐛 Issues: https://github.com/yourusername/athena/issues
echo 💬 Discussions: https://github.com/yourusername/athena/discussions
echo.
echo ⭐ If you find Athena helpful, star us on GitHub!
echo ============================================================