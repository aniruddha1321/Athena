# voice_interface.py - Robust Voice Interface with Proper Alignment

import streamlit as st
from src.voice_engine import AthenaVoice
import tempfile
import os
from datetime import datetime
import base64
import io
import wave


class VoiceInterface:
    """Streamlit-compatible voice interface with robust file handling"""
    
    def __init__(self):
        if 'voice_engine' not in st.session_state:
            try:
                # Use tiny model for faster loading (lazy loaded on first use)
                st.session_state.voice_engine = AthenaVoice(
                    whisper_model="tiny",
                    tts_lang='en'
                )
                st.session_state.voice_ready = True
                st.success("✅ Voice engine ready (model will load on first use)")
            except Exception as e:
                st.error(f"❌ Failed to initialize voice engine: {e}")
                st.session_state.voice_ready = False
        
        self.voice = st.session_state.voice_engine if st.session_state.get('voice_ready') else None
    
    def save_uploaded_audio(self, audio_data) -> str:
        """Save audio data to a proper WAV file"""
        try:
            # Create persistent temp directory
            temp_dir = os.path.join(tempfile.gettempdir(), "athena_voice")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            audio_path = os.path.join(temp_dir, f"recording_{timestamp}.wav")
            
            # Write audio data
            audio_bytes = audio_data.getvalue() if hasattr(audio_data, 'getvalue') else audio_data
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            # Verify file was created
            if not os.path.exists(audio_path):
                st.error(f"❌ Failed to create file at: {audio_path}")
                return None
            
            file_size = os.path.getsize(audio_path)
            
            if file_size == 0:
                st.error("❌ Audio file is empty (0 bytes)")
                return None
            
            st.success(f"✅ Audio saved: {file_size:,} bytes")
            print(f"✅ Audio file created:")
            print(f"   Path: {audio_path}")
            print(f"   Size: {file_size:,} bytes")
            print(f"   Exists: {os.path.exists(audio_path)}")
            
            return audio_path
            
        except Exception as e:
            st.error(f"❌ Error saving audio: {e}")
            import traceback
            st.code(traceback.format_exc())
            return None
    
    def transcribe_audio_safe(self, audio_path: str) -> dict:
        """Safely transcribe audio with comprehensive error checking"""
        
        # Check 1: File exists
        if not os.path.exists(audio_path):
            return {
                'success': False,
                'text': '',
                'error': f'File not found: {audio_path}'
            }
        
        # Check 2: File size
        file_size = os.path.getsize(audio_path)
        if file_size == 0:
            return {
                'success': False,
                'text': '',
                'error': 'Audio file is empty (0 bytes)'
            }
        
        st.info(f"📊 File ready: {os.path.basename(audio_path)} ({file_size:,} bytes)")
        
        # Check 3: Voice engine ready
        if not self.voice:
            return {
                'success': False,
                'text': '',
                'error': 'Voice engine not initialized'
            }
        
        # Transcribe
        try:
            with st.spinner("🎧 Transcribing (this may take 10-30 seconds)..."):
                result = self.voice.transcribe_audio(audio_path)
            
            if result.get('success'):
                st.success(f"✅ Transcribed: {result.get('confidence', 0):.0%} confidence")
                return result
            else:
                st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
                return result
                
        except Exception as e:
            error_msg = f"Transcription exception: {str(e)}"
            st.error(f"❌ {error_msg}")
            import traceback
            st.code(traceback.format_exc())
            
            return {
                'success': False,
                'text': '',
                'error': error_msg
            }
    
    def speak_response(self, text: str) -> str:
        """Generate speech with error handling"""
        if not self.voice:
            st.error("❌ Voice engine not available")
            return None
        
        # Limit text length for faster TTS
        if len(text) > 500:
            text = text[:500] + "..."
            st.info("📝 Response truncated to 500 characters for voice")
        
        try:
            with st.spinner("🔊 Generating speech (requires internet)..."):
                audio_file = self.voice.speak(text)
            
            if audio_file and os.path.exists(audio_file):
                st.success("✅ Voice response generated!")
                return audio_file
            else:
                st.warning("⚠️ TTS failed. Check internet connection.")
                return None
                
        except Exception as e:
            st.error(f"❌ TTS error: {e}")
            return None
    
    def play_audio(self, audio_file: str):
        """Display audio player"""
        if audio_file and os.path.exists(audio_file):
            try:
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/mp3')
            except Exception as e:
                st.error(f"❌ Error playing audio: {e}")


def render_voice_tab():
    """Voice interface with proper alignment and consistent styling"""
    
    # Header - consistent with other modules
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>🎙️ Voice Assistant</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 1.1em; margin-bottom: 1rem;'>Ask questions using your voice!</p>", unsafe_allow_html=True)
    
    # Check dependencies
    try:
        voice_interface = VoiceInterface()
        
        if not st.session_state.get('voice_ready'):
            st.error("❌ Voice engine failed to initialize")
            st.info("💡 Install dependencies: `pip install faster-whisper gtts soundfile`")
            return
            
    except Exception as e:
        st.error(f"❌ Voice interface error: {e}")
        st.info("💡 Install dependencies: `pip install faster-whisper gtts soundfile`")
        return
    
    # Voice history
    if 'voice_history' not in st.session_state:
        st.session_state.voice_history = []
    
    # PROPERLY ALIGNED: Settings, Mode, Clear in one row with equal heights
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Settings column with consistent height
    with col1:
        st.markdown("<p style='font-size: 1.1em; color: #64748b; margin-bottom: 0.2rem; font-weight: 500;'>Settings:</p>", unsafe_allow_html=True)
        auto_play = st.checkbox("🔊 Auto-play", value=True, key="voice_autoplay")
        show_text = st.checkbox("📝 Show text", value=True, key="voice_showtext")
    
    # Mode selection with increased height
    with col2:
        st.markdown("<p style='font-size: 1.1em; color: #64748b; margin-bottom: 0.2rem; margin-top: 0; font-weight: 500;'>Mode:</p>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            div[data-testid="stSelectbox"] {
                margin-top: -15px !important;
            }
            div[data-testid="stSelectbox"] div[data-baseweb="select"] {
                height: 48px !important;
                min-height: 48px !important;
            }
            div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                height: 48px !important;
                min-height: 48px !important;
                display: flex;
                align-items: center;
            }
            </style>
        """, unsafe_allow_html=True)
        query_mode = st.selectbox(
            "Mode",
            ["💬 Chat", "🔍 Search", "❓ Q&A"],
            key="voice_mode",
            label_visibility="collapsed"
        )

    # Clear button shifted upwards
    with col3:
        # Negative margin to shift button up
        st.markdown("<div style='margin-top: 22px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear", use_container_width=True, key="voice_clear"):
            st.session_state.voice_history = []
            st.success("Cleared!")
            st.rerun()

    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    # History section - compact
    if st.session_state.voice_history:
        st.markdown("<p style='font-weight: 600; font-size: 0.95em; color: #475569; margin-bottom: 0.5rem;'>💬 Recent Conversations</p>", unsafe_allow_html=True)
        
        for idx, exchange in enumerate(st.session_state.voice_history[-3:]):
            st.markdown(
                f"<div style='background: #f8fafc; padding: 0.8rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #3b82f6;'>"
                f"<strong style='color: #1e293b; font-size: 0.9em;'>🎤 You:</strong> "
                f"<span style='color: #475569; font-size: 0.9em;'>{exchange['question'][:80]}{'...' if len(exchange['question']) > 80 else ''}</span>"
                f"</div>",
                unsafe_allow_html=True
            )
            
            if show_text and exchange.get('response'):
                with st.expander("View Response", expanded=False):
                    st.markdown(
                        f"<div style='color: #475569; font-size: 0.9em; line-height: 1.6;'>{exchange['response'][:400]}{'...' if len(exchange['response']) > 400 else ''}</div>",
                        unsafe_allow_html=True
                    )
            
            if exchange.get('audio_file') and os.path.exists(exchange['audio_file']):
                st.audio(exchange['audio_file'])
        
        st.markdown("<hr style='margin: 0.8rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    
    # Input section
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>🎤 Record Your Question</h3>", unsafe_allow_html=True)
    
    # Mode description
    mode_help = {
        "💬 Chat": "💬 Natural conversation about the document",
        "🔍 Search": "🔍 Find specific sections or topics",
        "❓ Q&A": "❓ Get precise factual answers"
    }
    st.markdown(
        f"<div style='background: #eff6ff; padding: 0.5rem 0.7rem; border-radius: 6px; border-left: 3px solid #3b82f6; margin-bottom: 0.5rem;'>"
        f"<span style='color: #1e40af; font-size: 1.1em;'>{mode_help[query_mode]}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    # PROPERLY ALIGNED: Audio and text input in one row with equal heights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='font-size: 1.1em; color: #64748b; margin-bottom: 0.2rem; margin-top: 0; font-weight: 500;'>Record Audio:</p>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            div[data-testid="stAudioInput"] {
                height: 100px !important;
                margin-top: -10px !important;
            }
            div[data-testid="stAudioInput"] > div {
                height: 100px !important;
                display: flex;
                align-items: center;
            }
            </style>
        """, unsafe_allow_html=True)
        audio_data = st.audio_input("Record", label_visibility="collapsed", key="voice_audio")

    with col2:
        st.markdown("<p style='font-size: 1.1em; color: #64748b; margin-bottom: 0.2rem; margin-top: 0; font-weight: 500;'>Or type:</p>", unsafe_allow_html=True)
        st.markdown("""
            <style>
            div[data-testid="stTextArea"] {
                margin-top: -10px !important;
            }
            div[data-testid="stTextArea"] textarea {
                height: 100px !important;
                min-height: 100px !important;
            }
            </style>
        """, unsafe_allow_html=True)
        text_input = st.text_area(
            "Question", 
            label_visibility="collapsed", 
            placeholder="Type your question...",
            height=100,
            max_chars=500,
            key="voice_text"
        )

    # Submit button - compact spacing
    st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)
    
    # Process audio
    if audio_data is not None:
        if st.button("🎤 Answer (with voice)", key="process_audio", type="primary", use_container_width=True):
            with st.spinner("🎧 Transcribing audio..."):
                # Save audio
                audio_path = voice_interface.save_uploaded_audio(audio_data)
                
                if not audio_path:
                    st.error("❌ Failed to save audio file")
                    return
                
                # Transcribe
                result = voice_interface.transcribe_audio_safe(audio_path)
                
                if result['success'] and result['text'].strip():
                    question = result['text']
                    st.markdown(
                        f"<div style='background: #f0f9ff; padding: 0.6rem; border-radius: 6px; margin: 0.5rem 0;'>"
                        f"<strong style='color: #0c4a6e; font-size: 0.9em;'>📝 You asked:</strong> "
                        f"<span style='color: #075985; font-size: 0.9em;'>{question}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    
                    # Process query
                    process_query(question, voice_interface, query_mode, auto_play)
                    
                    # Cleanup
                    try:
                        os.unlink(audio_path)
                    except:
                        pass
                else:
                    st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
                    st.info("💡 Try speaking more clearly or check your microphone")
    
    # Process text input
    elif text_input.strip():
        if st.button("💬 Answer (with voice)", key="process_text", type="primary", use_container_width=True):
            process_query(text_input, voice_interface, query_mode, auto_play)


def process_query(question: str, voice_interface: VoiceInterface, 
                 query_mode: str, auto_play: bool):
    """Process query and generate response"""
    
    # Get response based on mode
    if query_mode == "💬 Chat":
        response_text = get_chat_response(question)
        mode_label = "Chat"
    elif query_mode == "🔍 Search":
        response_text = get_search_response(question)
        mode_label = "Search"
    else:
        response_text = get_qa_response(question)
        mode_label = "Q&A"
    
    if not response_text:
        return
    
    # Display response - consistent styling
    st.markdown(
        f"<div style='background: #f0fdf4; padding: 0.8rem; border-radius: 8px; border-left: 3px solid #22c55e; margin: 0.8rem 0;'>"
        f"<strong style='color: #15803d; font-size: 0.95em;'>🧠 Athena ({mode_label}):</strong>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    with st.expander("View Full Response", expanded=True):
        st.markdown(
            f"<div style='color: #475569; font-size: 0.9em; line-height: 1.6;'>{response_text}</div>",
            unsafe_allow_html=True
        )
    
    # Generate voice
    with st.spinner("🔊 Generating audio..."):
        audio_file = voice_interface.speak_response(response_text)
    
    if audio_file:
        # Save to history
        st.session_state.voice_history.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'question': question,
            'response': response_text,
            'audio_file': audio_file,
            'mode': mode_label
        })
        
        # Play
        if auto_play:
            st.audio(audio_file, autoplay=True)
        else:
            st.audio(audio_file)


def get_chat_response(question: str) -> str:
    """Get chat response"""
    if 'athena_chat' not in st.session_state:
        st.error("❌ Upload a document first!")
        return None
    
    with st.spinner("💭 Thinking..."):
        return st.session_state.athena_chat.chat(question)


def get_search_response(question: str) -> str:
    """Get semantic search response"""
    if 'semantic_index' not in st.session_state:
        st.error("❌ Build semantic index first (Semantic Search tab)")
        return None
    
    with st.spinner("🔍 Searching..."):
        from semantic_search import search_semantic
        results = search_semantic(st.session_state.semantic_index, question, k=3)
        
        if not results:
            return "No relevant sections found."
        
        response = f"Found {len(results)} relevant sections:\n\n"
        for i, (text, score) in enumerate(results, 1):
            response += f"{i}. ({score:.0%} match)\n{text[:150]}...\n\n"
        
        return response


def get_qa_response(question: str) -> str:
    """Get Q&A response"""
    if 'qa_chain' not in st.session_state:
        st.error("❌ Build Q&A index first (Q&A tab)")
        return None
    
    with st.spinner("❓ Finding answer..."):
        return st.session_state.qa_chain(question)


if __name__ == "__main__":
    st.set_page_config(page_title="Voice Test", page_icon="🎤")
    st.title("🎤 Voice Interface Test")
    render_voice_tab()