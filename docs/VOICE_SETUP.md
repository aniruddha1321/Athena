# 🎤 Voice Assistant - Setup Guide

## Overview
Athena includes a voice assistant that allows you to:
- 🎙️ **Ask questions using voice** (Speech-to-Text)
- 🔊 **Listen to answers** (Text-to-Speech)
- 💬 **Have natural conversations** with context awareness
- 🔍 **Search documents** using voice commands

## Quick Setup (Windows)

### 1. Run the Setup Script
```cmd
cd c:\Users\HP\Desktop\Proj\Athena
scripts\setup_voice.bat
```

### 2. Manual Installation (Alternative)
```cmd
pip install faster-whisper>=0.10.0
pip install gtts>=2.5.0
pip install soundfile>=0.12.1
```

## Quick Setup (Linux/Mac)

```bash
cd /path/to/Athena
bash scripts/setup_voice.sh
```

Or manually:
```bash
pip install faster-whisper gtts soundfile
```

## Features

### 🎙️ Speech-to-Text
- Uses **faster-whisper** (Windows-friendly, no FFmpeg needed!)
- Supports multiple languages
- Works offline after model download
- Models: `tiny`, `base`, `small`, `medium`, `large`

### 🔊 Text-to-Speech
- Uses **gTTS** (Google Text-to-Speech)
- Natural-sounding voices
- Requires internet connection
- Auto-play responses

### 💬 Voice Modes

1. **Chat Mode** - Natural conversation with context
2. **Search Mode** - Find relevant sections in documents
3. **Q&A Mode** - Precise answers from uploaded PDFs

## How to Use

1. **Start Athena**
   ```cmd
   streamlit run app.py
   ```

2. **Navigate to Voice tab** in the top menu

3. **Record your question**
   - Click the microphone button
   - Speak clearly
   - Stop recording

4. **Get voice response**
   - Athena transcribes your question
   - Processes it based on selected mode
   - Speaks the answer (auto-play enabled)

## Configuration

In the Voice tab Settings (⚙️):
- **Auto-play**: Automatically play audio responses
- **Mode**: Choose Chat, Search, or Q&A
- **Show text**: Display text versions of responses

## Troubleshooting

### "Voice engine failed to initialize"
```cmd
# Reinstall dependencies
pip uninstall faster-whisper gtts
pip install faster-whisper gtts soundfile
```

### "No module named 'faster_whisper'"
```cmd
pip install faster-whisper
```

### Audio recording not working
- Check microphone permissions
- Ensure microphone is connected and enabled
- Try browser refresh

### No audio playback
- Check system volume
- Try different browser (Chrome recommended)
- Enable auto-play in browser settings

## System Requirements

- **Python**: 3.8+
- **RAM**: 2GB+ (for base model)
- **Internet**: Required for gTTS (offline STT after model download)
- **Microphone**: For voice input
- **Speakers/Headphones**: For audio output

## Model Sizes (faster-whisper)

| Model  | Size  | RAM   | Speed | Accuracy |
|--------|-------|-------|-------|----------|
| tiny   | 39MB  | 1GB   | Fast  | Good     |
| base   | 74MB  | 1GB   | Fast  | Better   |
| small  | 244MB | 2GB   | Med   | Great    |
| medium | 769MB | 5GB   | Slow  | Excellent|

**Recommended for Windows**: `base` (best speed/accuracy balance)

## Privacy

- 🔒 **Speech-to-Text**: Runs locally (offline capable)
- 🌐 **Text-to-Speech**: Uses Google TTS (requires internet)
- 📝 **Conversations**: Stored in session only (not saved)

## Advanced Usage

### Change Whisper Model
Edit `src/voice_engine.py`:
```python
AthenaVoice(whisper_model="small")  # Change "base" to "small"
```

### Offline TTS (Alternative)
Replace gTTS with pyttsx3 for offline TTS:
```cmd
pip install pyttsx3
```

## Support

- 📖 See `docs/installation.md` for detailed setup
- 🐛 Report issues: `docs/bug_report.md`
- 💡 Request features: `docs/feature_request.md`
