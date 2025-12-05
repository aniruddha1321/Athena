#!/usr/bin/env python3
"""
Voice Engine Diagnostic Script
Tests all components to identify issues
"""

import sys
import os

print("=" * 70)
print("🔍 ATHENA VOICE ENGINE DIAGNOSTIC")
print("=" * 70)

# 1. Python Version
print(f"\n1️⃣ Python Version: {sys.version}")
if sys.version_info < (3, 8):
    print("   ❌ Python 3.8+ required")
    sys.exit(1)
else:
    print("   ✅ Python version OK")

# 2. Check Dependencies
print("\n2️⃣ Checking Dependencies...")

required = {
    'whisper': 'openai-whisper',
    'gtts': 'gtts',
    'streamlit': 'streamlit'
}

missing = []
for module, package in required.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - Install: pip install {package}")
        missing.append(package)

if missing:
    print(f"\n❌ Missing packages: {', '.join(missing)}")
    print(f"   Install with: pip install {' '.join(missing)}")
    sys.exit(1)

# 3. Test Whisper
print("\n3️⃣ Testing Whisper (Speech Recognition)...")
try:
    import whisper
    print("   Loading tiny model...")
    model = whisper.load_model("tiny")
    print("   ✅ Whisper loaded successfully")
    
    # Test with silence (if no audio file provided)
    import numpy as np
    silence = np.zeros(16000, dtype=np.float32)  # 1 second of silence
    
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    
    # Create minimal WAV file
    import wave
    with wave.open(temp_file.name, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        wav.writeframes((silence * 32767).astype(np.int16).tobytes())
    
    result = model.transcribe(temp_file.name, fp16=False)
    print(f"   ✅ Transcription test passed: '{result['text']}'")
    
    os.unlink(temp_file.name)
    
except Exception as e:
    print(f"   ❌ Whisper test failed: {e}")
    import traceback
    traceback.print_exc()

# 4. Test gTTS
print("\n4️⃣ Testing gTTS (Text-to-Speech)...")
try:
    from gtts import gTTS
    import tempfile
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_file.close()
    
    print("   Generating test audio (requires internet)...")
    tts = gTTS(text="Testing Athena voice engine", lang='en')
    tts.save(temp_file.name)
    
    if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 0:
        print(f"   ✅ TTS test passed: {os.path.getsize(temp_file.name)} bytes")
        os.unlink(temp_file.name)
    else:
        print("   ❌ TTS file not created")
        
except Exception as e:
    print(f"   ❌ TTS test failed: {e}")
    print("   💡 Make sure you have internet connection for gTTS")

# 5. Test Voice Engine
print("\n5️⃣ Testing Voice Engine Class...")
try:
    from voice_engine import AthenaVoice
    
    voice = AthenaVoice(whisper_model="tiny")
    print("   ✅ Voice engine initialized")
    
    # Test TTS
    print("   Testing speak()...")
    audio_file = voice.speak("Test", output_file="test_output.mp3")
    
    if audio_file and os.path.exists(audio_file):
        print(f"   ✅ speak() working: {os.path.getsize(audio_file)} bytes")
        os.unlink(audio_file)
    else:
        print("   ⚠️ speak() returned None (check internet)")
    
except Exception as e:
    print(f"   ❌ Voice engine test failed: {e}")
    import traceback
    traceback.print_exc()

# 6. File System Test
print("\n6️⃣ Testing File System...")
try:
    temp_dir = os.path.join(tempfile.gettempdir(), "athena_voice_test")
    os.makedirs(temp_dir, exist_ok=True)
    
    test_file = os.path.join(temp_dir, "test.txt")
    with open(test_file, 'w') as f:
        f.write("test")
    
    if os.path.exists(test_file):
        print(f"   ✅ File system working: {temp_dir}")
        os.unlink(test_file)
        os.rmdir(temp_dir)
    else:
        print("   ❌ File creation failed")
        
except Exception as e:
    print(f"   ❌ File system test failed: {e}")

# Summary
print("\n" + "=" * 70)
print("📊 DIAGNOSTIC SUMMARY")
print("=" * 70)

print("\n✅ What's Working:")
print("   - Python version")
print("   - Package imports")
print("   - Whisper model loading")

print("\n⚠️ Check These:")
print("   - Internet connection for gTTS")
print("   - Microphone permissions")
print("   - File system write permissions")

print("\n💡 Next Steps:")
print("   1. If all tests passed: streamlit run app.py")
print("   2. If TTS failed: Check internet connection")
print("   3. If Whisper failed: pip install --upgrade openai-whisper")

print("\n🎯 To test with real audio:")
print("   python test_voice.py your_audio_file.wav")

if len(sys.argv) > 1:
    audio_file = sys.argv[1]
    if os.path.exists(audio_file):
        print(f"\n📁 Testing with: {audio_file}")
        try:
            from voice_engine import AthenaVoice
            voice = AthenaVoice(whisper_model="tiny")
            result = voice.transcribe_audio(audio_file)
            
            print(f"\n📝 Transcription Result:")
            print(f"   Success: {result['success']}")
            print(f"   Text: {result['text']}")
            print(f"   Confidence: {result.get('confidence', 0):.0%}")
        except Exception as e:
            print(f"❌ Transcription failed: {e}")
    else:
        print(f"\n❌ File not found: {audio_file}")

print("\n" + "=" * 70)