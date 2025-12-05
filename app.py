import streamlit as st
from streamlit_option_menu import option_menu
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.paper_fetcher import research_topic, PaperFetcher
from src.qa_engine import make_qa_chain
from src.semantic_search import build_semantic_index, search_semantic
from src.pdf_utils import extract_text_from_pdf
from src.chat_engine import AthenaChat

# Importing Feature Modules
try:
    from src.document_comparison import DocumentComparison
    COMPARISON_AVAILABLE = True
except ImportError:
    COMPARISON_AVAILABLE = False

try:
    from src.voice_interface import render_voice_tab
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    from src.kg_visualizer import render_knowledge_graph_tab
    from src.advanced_rag import AdvancedRAG
    KG_RAG_AVAILABLE = True
except ImportError:
    KG_RAG_AVAILABLE = False

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Athena - AI Research Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS (Style) ----------
hide_streamlit_style = """
    <style>
    /* Hide Streamlit branding */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    div.block-container {padding-top: 1rem;}
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(71, 85, 105, 0.25);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(71, 85, 105, 0.4);
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #f8fafc;
        border-left: 4px solid #64748b;
        padding: 1rem;
        border-radius: 8px;
        color: #1e293b;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #f8fafc;
        border-left: 4px solid #64748b;
        padding: 1rem;
        border-radius: 8px;
        color: #1e293b;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #f8fafc;
        border: 2px dashed #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
    }
    
    /* Text input */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #cbd5e1;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #475569;
        box-shadow: 0 0 0 3px rgba(71, 85, 105, 0.1);
        outline: none;
    }
    
    /* Text area */
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #cbd5e1;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stTextArea>div>div>textarea:focus {
        border-color: #475569;
        box-shadow: 0 0 0 3px rgba(71, 85, 105, 0.1);
        outline: none;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8fafc;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #475569 0%, #334155 100%);
        color: white;
    }
    
    /* Result boxes */
    .result-box {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        line-height: 1.8;
        color: #1e293b;
        font-size: 1.05rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .answer-box {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #64748b;
        line-height: 1.8;
        color: #1e293b;
        font-size: 1.05rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .comparison-box {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #64748b;
        line-height: 1.8;
        color: #1e293b;
        font-size: 1.05rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .rag-box {
        background-color: #fef3c7;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        line-height: 1.8;
        color: #92400e;
        font-size: 1.05rem;
        border: 1px solid #fde68a;
        margin: 1rem 0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #f9fafb;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------- Initialize Session State ----------
def init_session_state():
    if "athena_chat" not in st.session_state:
        st.session_state.athena_chat = AthenaChat(model="llama3.2:1b", temperature=0.3)
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    if "pdf_uploaded" not in st.session_state:
        st.session_state.pdf_uploaded = False
    
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    
    if COMPARISON_AVAILABLE and "doc_comparison" not in st.session_state:
        st.session_state.doc_comparison = DocumentComparison(model="llama3.2:1b")
    
    if KG_RAG_AVAILABLE and "advanced_rag" not in st.session_state:
        st.session_state.advanced_rag = AdvancedRAG(chunk_size=800, chunk_overlap=100)
    
    if 'menu_selection' not in st.session_state:
        st.session_state.menu_selection = "Home"

# ---------- Sidebar ----------
def render_sidebar():
    # Sidebar logo
    sidebar_style = """
        <style>
        /* Sidebar background and styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 2px solid #e2e8f0;
        }
        section[data-testid="stSidebar"] > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        section[data-testid="stSidebar"] > div > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        section[data-testid="stSidebar"] div:has(img) {
            padding-top: 0 !important;
            margin-top: -7px !important;
        }
        
        /* Sidebar headings */
        section[data-testid="stSidebar"] h2 {
            color: #1e293b;
            font-weight: 700;
            margin-top: 1.5rem;
        }
        
        /* Sidebar text */
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] li {
            color: #475569;
        }
        
        /* Sidebar success/error boxes */
        section[data-testid="stSidebar"] .stSuccess,
        section[data-testid="stSidebar"] .stError,
        section[data-testid="stSidebar"] .stWarning {
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.5rem 0;
        }
        
        section[data-testid="stSidebar"] .stSuccess {
            background-color: #f0fdf4;
            border-left: 4px solid #22c55e;
            color: #15803d;
        }
        
        section[data-testid="stSidebar"] .stError {
            background-color: #fef2f2;
            border-left: 4px solid #ef4444;
            color: #991b1b;
        }
        
        section[data-testid="stSidebar"] .stWarning {
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            color: #92400e;
        }
        
        /* Sidebar buttons */
        section[data-testid="stSidebar"] .stButton>button {
            background: linear-gradient(135deg, #475569 0%, #334155 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            box-shadow: 0 2px 6px rgba(71, 85, 105, 0.25);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        section[data-testid="stSidebar"] .stButton>button:hover {
            background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
            box-shadow: 0 4px 12px rgba(71, 85, 105, 0.4);
            transform: translateY(-2px);
        }
        
        /* Ensure button text is white */
        section[data-testid="stSidebar"] .stButton>button p {
            color: white !important;
        }
        </style>
    """
    st.markdown(sidebar_style, unsafe_allow_html=True)

    hide_sidebar_button = """
    <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }
    </style>
    """
    st.markdown(hide_sidebar_button, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div style="margin-top: 50px;"></div>', unsafe_allow_html=True)
        st.image(
            "assets/athena.png",
            width=265,
            use_container_width=False
        )
        # st.markdown("---")
        st.markdown("<h2 style='margin-top: 0.5rem; margin-bottom: 0.5rem;'>ℹ️ About</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-top: 0.3rem; line-height: 1.5;'>
        <strong>Athena</strong> is a local AI research assistant that helps you:
        </div>
        <ul style='margin-top: 0.3rem; margin-bottom: 0.5rem; line-height: 1.4;'>
        <li>Analyze research papers</li>
        <li>Extract key insights</li>
        <li>Build knowledge graphs</li>
        <li>Compare multiple documents</li>
        <li>Ask contextual questions</li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 0.8rem 0; border: none; border-top: 2px solid #e2e8f0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='margin-top: 0.5rem; margin-bottom: 0.5rem;'>ℹ️ System Status</h2>", unsafe_allow_html=True)
        
        # Check Ollama status
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                st.success("llama: Running")
                models = response.json().get('models', [])
                if any('llama3.2:1b' in m.get('name', '') for m in models):
                    st.success("llama3.2:1b: Available")
                else:
                    st.warning("llama3.2:1b: Not found")
            else:
                st.error("Ollama: Error")
        except:
            st.error("Ollama: Not running")
            st.caption("Start: `ollama serve`")
        
        # Session stats
        if st.session_state.pdf_uploaded:
            st.markdown("<hr style='margin: 0.8rem 0; border: none; border-top: 2px solid #e2e8f0;'>", unsafe_allow_html=True)
            st.markdown("<h2 style='margin-top: 0.5rem; margin-bottom: 0.5rem;'>📊 Session Stats</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>Document:</strong> {st.session_state.get('pdf_filename', 'N/A')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>Text length:</strong> {len(st.session_state.pdf_text):,} chars</p>", unsafe_allow_html=True)
            
            if 'qa_chain' in st.session_state:
                st.markdown("<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>Q&A Index:</strong> Ready</p>", unsafe_allow_html=True)
            
            if 'semantic_index' in st.session_state:
                st.markdown("<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>Semantic Index:</strong> Ready</p>", unsafe_allow_html=True)
            
            if KG_RAG_AVAILABLE and 'kg_builder' in st.session_state:
                summary = st.session_state.kg_builder.get_graph_summary()
                st.markdown(f"<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>Knowledge Graph:</strong> {summary['total_nodes']} nodes</p>", unsafe_allow_html=True)
            
            if KG_RAG_AVAILABLE:
                rag_summary = st.session_state.advanced_rag.get_document_summary()
                st.markdown(f"<p style='margin: 0.2rem 0; line-height: 1.4;'><strong>RAG Documents:</strong> {rag_summary['total_documents']}</p>", unsafe_allow_html=True)
        
        # Reset button
        st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
        if st.button("Reset Session", key="reset_session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("Session reset! Refreshing...")
            st.rerun()

# ---------- Main Application ----------
def main():
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Navigation helper - use query params instead of session state to avoid conflicts
    if 'nav_target' not in st.session_state:
        st.session_state.nav_target = None
    
    def nav_to_research():
        st.session_state.nav_target = "Research"
    
    def nav_to_qa():
        st.session_state.nav_target = "Q&A"
    
    def nav_to_search():
        st.session_state.nav_target = "Search"
    
    def nav_to_chat():
        st.session_state.nav_target = "Chat"
    
    # Apply navigation target before menu renders
    if st.session_state.nav_target:
        st.session_state.menu_selection = st.session_state.nav_target
        st.session_state.nav_target = None
    
    # Build menu options dynamically
    menu_options = ["Home", "Research", "Q&A", "Search", "Chat"]
    menu_icons = ["house", "file-text", "question-circle", "search", "chat-dots"]
    
    if KG_RAG_AVAILABLE:
        menu_options.extend(["KG", "RAG"])
        menu_icons.extend(["diagram-3", "layers"])
    
    if COMPARISON_AVAILABLE:
        menu_options.append("Compare")
        menu_icons.append("files")
    
    if VOICE_AVAILABLE:
        menu_options.append("Voice")
        menu_icons.append("mic")
    
    # Horizontal navigation menu - use manual_select to sync with buttons
    current_index = menu_options.index(st.session_state.menu_selection)
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=current_index,
        orientation="horizontal",
        key='menu_selection',
        manual_select=current_index,  # Force sync with session state
        styles={
            "container": {"padding": "0!important", "background-color": "#ffffff", "box-shadow": "0 2px 6px rgba(0,0,0,0.12)"},
            "icon": {"color": "#94a3b8", "font-size": "24px", "font-weight": "bold"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 15px",
                "color": "#64748b",
                "font-weight": "600",
                "--hover-color": "#f1f5f9",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #475569 0%, #334155 100%)",
                "color": "white",
                "font-weight": "700",
                "box-shadow": "0 3px 12px rgba(71, 85, 105, 0.4)"
            },
        }
    )
    
    # ---------- HOME PAGE ----------
    if selected == "Home":
        st.markdown(
            "<p style='text-align: center; font-size: 1.3em; color: #1e293b; font-weight: 500; margin-bottom: 0.5rem;'><strong style='color: #1e293b; font-size: 1.15em;'>Athena</strong>: Your Local AI Research Assistant</p>"
            "<hr style='margin: 0 auto; width: 60%; border: none; border-top: 2px solid #e2e8f0;'>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                "<div style='background: linear-gradient(to bottom, #ffffff 0%, #eff6ff 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 1rem; border: 1px solid #bfdbfe; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);'>"
                "<strong style='color: #1e3a8a; font-size: 1.15em;'>📄 Research & Summarize</strong><br>"
                "<span style='color: #1e40af; font-size: 0.95em;'>Upload PDFs or enter research topics to get comprehensive AI-generated summaries. Athena analyzes papers, extracts key insights, and presents findings in clear, structured formats.</span>"
                "</div>",
                unsafe_allow_html=True
            )
            st.button("Start Research", on_click=nav_to_research, use_container_width=True)
        
        with col2:
            st.markdown(
                "<div style='background: linear-gradient(to bottom, #ffffff 0%, #f0fdf4 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #10b981; margin-bottom: 1rem; border: 1px solid #bbf7d0; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);'>"
                "<strong style='color: #065f46; font-size: 1.15em;'>💬 Smart Q&A</strong><br>"
                "<span style='color: #047857; font-size: 0.95em;'>Ask specific questions about your research documents and get accurate, context-aware answers. Our AI retrieves relevant information and provides detailed responses with source attribution.</span>"
                "</div>",
                unsafe_allow_html=True
            )
            st.button("Ask Questions", on_click=nav_to_qa, use_container_width=True)
        
        with col3:
            st.markdown(
                "<div style='background: linear-gradient(to bottom, #ffffff 0%, #fef3c7 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #f59e0b; margin-bottom: 1rem; border: 1px solid #fde68a; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);'>"
                "<strong style='color: #92400e; font-size: 1.15em;'>🔍 Semantic Search</strong><br>"
                "<span style='color: #b45309; font-size: 0.95em;'>Search for concepts and ideas within your documents using AI-powered semantic understanding. Find relevant content even when exact keywords don't match, & discover conn. across your research papers.</span>"
                "</div>",
                unsafe_allow_html=True
            )
            st.button("Search Documents", on_click=nav_to_search, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Additional features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                "<div style='background: linear-gradient(to bottom, #ffffff 0%, #faf5ff 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #a855f7; margin-bottom: 1rem; border: 1px solid #e9d5ff; box-shadow: 0 2px 8px rgba(168, 85, 247, 0.15);'>"
                "<strong style='color: #6b21a8; font-size: 1.15em;'>🤖 Chat Interface</strong><br>"
                "<span style='color: #7e22ce; font-size: 0.95em;'>Have natural conversations with Athena about research topics. The AI maintains context and provides thoughtful, detailed responses to complex queries.</span>"
                "</div>",
                unsafe_allow_html=True
            )
            st.button("Start Chatting", on_click=nav_to_chat, use_container_width=True)
        
        with col2:
            if KG_RAG_AVAILABLE:
                st.markdown(
                    "<div style='background: linear-gradient(to bottom, #ffffff 0%, #fef2f2 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #ef4444; margin-bottom: 1rem; border: 1px solid #fecaca; box-shadow: 0 2px 8px rgba(239, 68, 68, 0.15);'>"
                    "<strong style='color: #991b1b; font-size: 1.15em;'>🕸️ Knowledge Graphs</strong><br>"
                    "<span style='color: #b91c1c; font-size: 0.95em;'>Visualize relationships between concepts, entities, and ideas in your research. Build interactive knowledge graphs to explore connections.</span>"
                    "</div>",
                    unsafe_allow_html=True
                )
                if st.button("Explore Graphs", use_container_width=True, key="nav_kg_from_home"):
                    st.session_state.nav_target = "KG"
                    st.rerun()
            else:
                st.markdown(
                    "<div style='background: linear-gradient(to bottom, #fef3c7 0%, #fde68a 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #f59e0b; margin-bottom: 1rem; border: 1px solid #fde68a; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.15);'>"
                    "<strong style='color: #92400e; font-size: 1.15em;'>📊 Advanced Analytics</strong><br>"
                    "<span style='color: #92400e; font-size: 0.95em;'>Unlock deeper insights with multi-document analysis, concept tracking, and cross-paper comparisons. (Install optional dependencies)</span>"
                    "</div>",
                    unsafe_allow_html=True
                )
        
        with col3:
            if COMPARISON_AVAILABLE:
                st.markdown(
                    "<div style='background: linear-gradient(to bottom, #ffffff 0%, #ecfeff 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #06b6d4; margin-bottom: 1rem; border: 1px solid #a5f3fc; box-shadow: 0 2px 8px rgba(6, 182, 212, 0.15);'>"
                    "<strong style='color: #164e63; font-size: 1.15em;'>📑 Document Comparison</strong><br>"
                    "<span style='color: #0e7490; font-size: 0.95em;'>Compare multiple research papers side-by-side. Identify similarities, differences, and unique contributions across documents.</span>"
                    "</div>",
                    unsafe_allow_html=True
                )
                if st.button("Compare Papers", use_container_width=True, key="nav_compare_from_home"):
                    st.session_state.nav_target = "Compare"
                    st.rerun()
            else:
                st.markdown(
                    "<div style='background: linear-gradient(to bottom, #ffffff 0%, #fce7f3 100%); padding: 1.2rem; border-radius: 10px; border-left: 5px solid #ec4899; margin-bottom: 1rem; border: 1px solid #fbcfe8; box-shadow: 0 2px 8px rgba(236, 72, 153, 0.15);'>"
                    "<strong style='color: #831843; font-size: 1.15em;'>✨ Personalized Research</strong><br>"
                    "<span style='color: #9f1239; font-size: 0.95em;'>Athena learns from your queries and adapts to your research style, providing increasingly relevant and targeted insights.</span>"
                    "</div>",
                    unsafe_allow_html=True
                )
    
    # ---------- RESEARCH PAGE ----------
    elif selected == "Research":
        # Custom CSS to remove default spacing
        st.markdown("""
            <style>
            div[data-testid="column"] > div > div > div > div {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                margin-top: 0 !important;
                margin-bottom: 0.5rem !important;
            }
            div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
                margin-top: 0 !important;
                margin-bottom: 0.3rem !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: -1rem;'></div>", unsafe_allow_html=True)
        
        # Create two columns - left for functionality, right for guidelines
        left_col, right_col = st.columns([1.2, 0.8])
        
        with left_col:
            st.markdown(
                "<h2 style='color: #1f2937; font-size: 1.8em; font-weight: 600; margin-bottom: 0.5rem;'>📄 Research & Summarize</h2>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<p style='color: #9ca3af; font-size: 1em; margin-bottom: 0.5rem;'>Upload a research paper (PDF) or enter a topic to get started</p>",
                unsafe_allow_html=True
            )
            
            # File upload section
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type="pdf",
                key="main_pdf_upload"
            )
            
            st.markdown(
                "<p style='color: #9ca3af; font-size: 1em; margin: 0.3rem 0 0.2rem 0; font-weight: 400;'>Or enter a research topic below</p>",
                unsafe_allow_html=True
            )
            
            # Research topic input
            topic = st.text_input(
                "Research Topic",
                placeholder="e.g., Recent advances in transformer architectures",
                key="research_topic_input",
                label_visibility="collapsed"
            )
            
            # Start Research button
            start_research = st.button("Start Research", type="primary", use_container_width=True, key="start_research_btn")
        
        with right_col:
            st.markdown(
                "<div style='background: linear-gradient(to bottom, #ffffff 0%, #f8fafc 100%); padding: 1.2rem 1.5rem 1rem 1.5rem; border-radius: 12px; border-left: 5px solid #475569; box-shadow: 0 2px 8px rgba(71, 85, 105, 0.12); margin-top: 0;'>"
                "<h3 style='color: #1e293b; margin: 0 0 0.5rem 0; font-size: 1.8em; font-weight: 600;'>How to Use?</h3>"
                "<div style='color: #475569; font-size: 1.05em; line-height: 1.6;'>"
                "<strong style='color: #1e293b; display: block; margin: 0 0 0.2rem 0; font-size: 1.1em;'>PDF Upload:</strong>"
                "<div style='margin: 0 0 0.5rem 0;'>"
                "<span style='color: #64748b;'>•</span> Max file size: 200MB<br>"
                "<span style='color: #64748b;'>•</span> Supports text-based PDFs<br>"
                "<span style='color: #64748b;'>•</span> Extracts and summarizes content"
                "</div>"
                "<strong style='color: #1e293b; display: block; margin: 0 0 0.2rem 0; font-size: 1.1em;'>Topic Research:</strong>"
                "<div style='margin: 0 0 0.5rem 0;'>"
                "<span style='color: #64748b;'>•</span> Enter any research topic<br>"
                "<span style='color: #64748b;'>•</span> Fetches papers from arXiv<br>"
                "<span style='color: #64748b;'>•</span> Generates comprehensive summaries"
                "</div>"
                "<strong style='color: #1e293b; display: block; margin: 0 0 0.2rem 0; font-size: 1.1em;'>Tips:</strong>"
                "<div style='margin: 0;'>"
                "<span style='color: #64748b;'>•</span> Be specific with topics<br>"
                "<span style='color: #64748b;'>•</span> Check Ollama status in sidebar<br>"
                "<span style='color: #64748b;'>•</span> Results available in all tabs<br>"
                "<span style='color: #64748b;'>•</span> Use Q&A for specific questions<br>"
                "<span style='color: #64748b;'>•</span> Chat interface maintains context"
                "</div>"
                "</div>"
                "</div>",
                unsafe_allow_html=True
            )
        
        # Continue with the functionality below columns
        if start_research:
            if topic.strip() == "" and not uploaded_file:
                st.markdown('<p style="color: red;">Please enter a topic or upload a PDF.</p>', unsafe_allow_html=True)
            else:
                with st.spinner("🔍 Analyzing document and generating summary..."):
                    if uploaded_file:
                        try:
                            text = extract_text_from_pdf(uploaded_file)
                            
                            if not text.strip():
                                st.markdown('<p style="color: red;">Could not extract text from PDF.</p>', unsafe_allow_html=True)
                                st.stop()
                            
                            st.session_state.pdf_text = text
                            st.session_state.pdf_uploaded = True
                            st.session_state.pdf_filename = uploaded_file.name
                            
                            splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
                            chunks = splitter.split_text(text)
                            
                            summaries = []
                            progress_bar = st.progress(0)
                            
                            for i, chunk in enumerate(chunks):
                                partial_query = f"Summarize this section:\n\n{chunk}"
                                chunk_summary = research_topic(partial_query, skip_tools=True)
                                summaries.append(chunk_summary)
                                progress_bar.progress((i + 1) / len(chunks))
                            
                            combined_text = "\n\n".join(summaries)
                            final_query = f"Create a cohesive summary:\n\n{combined_text}"
                            result = research_topic(final_query, skip_tools=True)
                        
                        except Exception as e:
                            st.markdown('<p style="color: red;">Error processing PDF: {}</p>'.format(e), unsafe_allow_html=True)
                            st.stop()
                    
                    else:
                        try:
                            result = research_topic(topic)
                            
                            # Check if result contains an error message
                            if result.startswith("Error:"):
                                st.error(f"{result}")
                                
                                # Provide helpful suggestions
                                if "status 500" in result:
                                    st.warning("**Possible causes:**")
                                    st.markdown("""
                                    - The prompt may be too long for the model's context window
                                    - The model might be out of memory
                                    - Try a shorter topic or simpler query
                                    - Check Ollama logs: `ollama logs` in terminal
                                    """)
                                    st.info("**Quick fix:** Try restarting Ollama with `ollama serve`")
                                elif "Connection" in result or "connect" in result:
                                    st.warning("Ollama doesn't appear to be running.")
                                    st.code("ollama serve", language="bash")
                                elif "timed out" in result:
                                    st.warning("The request took too long. Try a simpler query or check if Ollama is overloaded.")
                                
                                st.stop()
                            
                            st.session_state.pdf_text = result
                            st.session_state.pdf_uploaded = True
                            st.session_state.pdf_filename = f"{topic[:30]}.txt"
                        except Exception as e:
                            st.error(f"Error during research: {e}")
                            st.stop()
                    
                    st.session_state.last_result = result
                    st.session_state.athena_chat.set_pdf_context(st.session_state.pdf_text)
                    st.success("Research complete! Results available in all tabs.")
                    st.rerun()
        
        # Display results
        if st.session_state.last_result:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(
                "<h3 style='color: #111827;'>Summary Results</h3>",
                unsafe_allow_html=True
            )
            st.markdown(f"<div class='result-box'>{st.session_state.last_result}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="Download Summary",
                    data=st.session_state.last_result,
                    file_name="athena_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                st.button("Ask Questions", on_click=nav_to_qa, use_container_width=True, key="nav_qa_from_research", type="primary")
            
            with col3:
                st.button("Start Chat", on_click=nav_to_chat, use_container_width=True, key="nav_chat_from_research", type="primary")
    
    # ---------- Q&A PAGE ----------
    elif selected == "Q&A":
        st.markdown("### Question & Answer")
        
        if not st.session_state.pdf_uploaded:
            st.warning("No document loaded. Please upload a document first.")
            st.button("Go to Research", on_click=nav_to_research, use_container_width=True)
        else:
            st.info(f"Active Document: **{st.session_state.get('pdf_filename', 'Unknown')}**")
            
            if "qa_chain" not in st.session_state:
                with st.spinner("Building Q&A index..."):
                    try:
                        qa_function = make_qa_chain(
                            st.session_state.pdf_text,
                            chunk_size=2000,
                            k=3,
                            model="llama3.2:1b"
                        )
                        st.session_state.qa_chain = qa_function
                        st.success("Q&A system ready!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()
            
            query = st.text_input(
                "Your Question",
                placeholder="e.g., What methodology was used in this study?",
                key="qa_question_input"
            )
            
            if st.button("Get Answer", type="primary", use_container_width=True):
                if query.strip() == "":
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Analyzing document..."):
                        try:
                            answer = st.session_state.qa_chain(query)
                            st.markdown("### Answer")
                            st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
    
    # ---------- SEARCH PAGE ----------
    elif selected == "Search":
        st.markdown("### Semantic Search")
        
        if not st.session_state.pdf_uploaded:
            st.warning("No document loaded. Please upload a document first.")
            st.button("Go to Research", on_click=nav_to_research, use_container_width=True)
        else:
            st.info(f"Active Document: **{st.session_state.get('pdf_filename', 'Unknown')}**")
            
            if "semantic_index" not in st.session_state:
                with st.spinner("Building semantic index..."):
                    try:
                        vectordb = build_semantic_index(
                            st.session_state.pdf_text,
                            chunk_size=300,
                            chunk_overlap=50
                        )
                        st.session_state.semantic_index = vectordb
                        st.success("Search index ready!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.stop()
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                query = st.text_input(
                    "Search Query",
                    placeholder="e.g., attention mechanism implementation",
                    key="semantic_search_input"
                )
            
            with col2:
                num_results = st.selectbox("Results", [5, 10, 15, 20], index=0)
            
            if st.button("Search", type="primary", use_container_width=True):
                if not query.strip():
                    st.warning("Please enter a search query.")
                else:
                    with st.spinner("Searching..."):
                        try:
                            results = search_semantic(
                                st.session_state.semantic_index,
                                query,
                                k=num_results
                            )
                            
                            if not results:
                                st.warning("No relevant matches found.")
                            else:
                                st.session_state.semantic_results = results
                                st.success(f"Found {len(results)} results")
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            if "semantic_results" in st.session_state and st.session_state.semantic_results:
                st.markdown("---")
                st.markdown("### Search Results")
                
                min_similarity = st.slider(
                    "Minimum Similarity",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.3,
                    step=0.05
                )
                
                filtered_results = [
                    (text, score) for text, score in st.session_state.semantic_results
                    if score >= min_similarity
                ]
                
                if not filtered_results:
                    st.warning(f"No results above {min_similarity:.0%} similarity")
                else:
                    st.info(f"Showing {len(filtered_results)} results")
                    
                    for i, (text, similarity) in enumerate(filtered_results, 1):
                        if similarity >= 0.7:
                            color = "🟢"
                        elif similarity >= 0.5:
                            color = "🟡"
                        else:
                            color = "🟠"
                        
                        with st.expander(f"{color} Result {i} - Similarity: {similarity:.0%}", expanded=(i<=3)):
                            st.markdown(text)
    
    # ---------- CHAT PAGE ----------
    elif selected == "Chat":
        st.markdown("<h3 style='margin-bottom: 0.5rem;'>💬 Chat with Athena</h3>", unsafe_allow_html=True)
        
        if not st.session_state.pdf_uploaded:
            st.info("💡 Start chatting! Athena can discuss research topics, answer questions, and provide insights.")
        else:
            st.info(f"💡 Athena has loaded: **{st.session_state.get('pdf_filename', 'your document')}**")
        
        col1, col2 = st.columns([4, 1])
        
        with col2:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.athena_chat.clear_history()
                st.session_state.chat_messages = []
                st.success("Chat cleared!")
                st.rerun()
        
        st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
        
        # Display chat history
        for msg in st.session_state.chat_messages:
            with st.chat_message("user"):
                st.markdown(msg["user"])
            
            with st.chat_message("assistant", avatar="🧠"):
                st.markdown(msg["assistant"])
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        if user_input and user_input.strip():
            with st.spinner("Athena is thinking..."):
                response = st.session_state.athena_chat.chat(user_input)
                
                st.session_state.chat_messages.append({
                    "user": user_input,
                    "assistant": response
                })
                
                st.rerun()
    
    # ---------- KNOWLEDGE GRAPH PAGE (Optional) ----------
    elif selected == "KG":
        if KG_RAG_AVAILABLE:
            if st.session_state.pdf_uploaded:
                render_knowledge_graph_tab(
                    st.session_state.pdf_text,
                    title=st.session_state.get('pdf_filename', 'Research Document')
                )
            else:
                st.warning("No document loaded. Please upload a document first.")
                st.button("Go to Research", on_click=nav_to_research, use_container_width=True)
        else:
            st.markdown("### 🕸️ Knowledge Graphs")
            st.error("⚠️ Knowledge Graph feature requires additional dependencies")
            st.info("""
            To enable this feature, install the optional dependencies:
            
            ```bash
            pip install -r requirements_kg_rag.txt
            ```
            
            Or install manually:
            ```bash
            pip install networkx spacy
            python -m spacy download en_core_web_sm
            ```
            """)
            st.button("Go to Research", on_click=nav_to_research, use_container_width=True, type="primary")
    
    # ---------- ADVANCED RAG PAGE (Optional) ----------
    elif selected == "Adv. RAG":
        if not KG_RAG_AVAILABLE:
            st.markdown("### 📚 Advanced Multi-Document RAG")
            st.error("⚠️ Advanced RAG feature requires additional dependencies")
            st.info("""
            To enable this feature, install the optional dependencies:
            
            ```bash
            pip install -r requirements_kg_rag.txt
            ```
            
            This will enable:
            - Multi-document query support
            - Cross-document analysis
            - Source attribution
            - Advanced context retrieval
            """)
            st.button("Go to Research", on_click=nav_to_research, use_container_width=True, type="primary")
        elif KG_RAG_AVAILABLE:
            st.markdown("### Advanced Multi-Document RAG")
            st.info("Ask questions across multiple documents with source attribution")
            
            # RAG implementation (abbreviated for space)
            if st.session_state.pdf_uploaded:
                rag = st.session_state.advanced_rag
                
                if st.button("Add Current Document", type="primary"):
                    doc_id = st.session_state.get('pdf_filename', 'document_1')
                    with st.spinner("Adding document..."):
                        rag.add_document(
                            doc_id=doc_id,
                            title=doc_id,
                            content=st.session_state.pdf_text,
                            metadata={'type': 'research_paper'}
                        )
                    st.success(f"Added: {doc_id}")
                    st.rerun()
                
                summary = rag.get_document_summary()
                
                if summary['total_documents'] > 0:
                    st.markdown(f"**Loaded Documents:** {summary['total_documents']}")
                    
                    # Query interface
                    rag_query = st.text_input(
                        "Ask a question across all documents",
                        placeholder="e.g., Compare the methodologies used",
                        key="rag_query"
                    )
                    
                    if st.button("Answer", type="primary", use_container_width=True):
                        if rag_query:
                            with st.spinner("Analyzing..."):
                                result = rag.answer_with_context(rag_query, k=5)
                            
                            st.markdown("### Answer")
                            st.markdown(f"**Confidence:** {result['confidence']:.0%}")
                            st.markdown(f"<div class='rag-box'>{result['answer']}</div>", unsafe_allow_html=True)
                else:
                    st.warning("No documents loaded yet. Add documents to use RAG.")
            else:
                st.warning("No document loaded. Please upload a document first.")
                st.button("Go to Research", on_click=nav_to_research, use_container_width=True)
    
    # ---------- COMPARISON PAGE (Optional) ----------
    elif selected == "Compare" and COMPARISON_AVAILABLE:
        st.markdown("### Document Comparison")
        st.info("Upload two PDFs to compare side-by-side")
        
        col1, col2 = st.columns(2)
        
        with col1:
            doc1_file = st.file_uploader("Document 1", type="pdf", key="doc1")
        
        with col2:
            doc2_file = st.file_uploader("Document 2", type="pdf", key="doc2")
        
        if st.button("Compare", type="primary", use_container_width=True):
            if not doc1_file or not doc2_file:
                st.warning("Please upload both documents.")
            else:
                with st.spinner("Comparing documents..."):
                    try:
                        text1 = extract_text_from_pdf(doc1_file)
                        text2 = extract_text_from_pdf(doc2_file)
                        
                        st.session_state.doc_comparison.add_document(doc1_file.name, text1)
                        st.session_state.doc_comparison.add_document(doc2_file.name, text2)
                        
                        comparison_result = st.session_state.doc_comparison.compare_documents(
                            doc1_file.name,
                            doc2_file.name
                        )
                        st.session_state.comparison_result = comparison_result
                        st.success("Comparison complete!")
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        if "comparison_result" in st.session_state and st.session_state.comparison_result:
            result = st.session_state.comparison_result
            
            st.markdown("---")
            st.markdown("### Comparison Results")
            st.markdown(f"<div class='comparison-box'>{result['summary']}</div>", unsafe_allow_html=True)
            
            with st.expander("Similarities", expanded=True):
                st.markdown(result['similarities'])
            
            with st.expander("Differences", expanded=True):
                st.markdown(result['differences'])
    
    # ---------- VOICE PAGE (Optional) ----------
    elif selected == "Voice" and VOICE_AVAILABLE:
        render_voice_tab()

# ---------- Run Application ----------
if __name__ == "__main__":
    main()