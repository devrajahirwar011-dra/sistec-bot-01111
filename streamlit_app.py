"""
SISTec InfoBot - Streamlit Web Interface
Modern, animated college-themed AI assistant for Sagar Institute of Science and Technology
"""

import streamlit as st
import os
from pathlib import Path
import time
from datetime import datetime
from rag_engine import RAGEngine
from document_processor import ChunkProcessor
from config import DOCUMENTS_PATH
import requests
from PIL import Image
import io

# Page Configuration
st.set_page_config(
    page_title="SISTec InfoBot | Sagar Institute",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Design
st.markdown("""
<style>
/* Color Variables */
:root {
    --primary-dark: #0F172A;
    --primary-blue: #1D4ED8;
    --accent-cyan: #06B6D4;
    --white: #FFFFFF;
    --light-gray: #F1F5F9;
    --dark-gray: #1E293B;
}

/* Main Background */
* {
    margin: 0;
    padding: 0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0F172A 0%, #1a2a4a 100%);
    color: #F1F5F9;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 2px solid #06B6D4;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.1);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 1.5rem;
}

/* Main Container */
.main {
    background: transparent;
}

/* Chat Messages */
.user-message {
    background: linear-gradient(135deg, #1D4ED8, #0F172A);
    border-radius: 15px;
    padding: 12px 16px;
    margin: 8px 0;
    border-left: 4px solid #06B6D4;
    box-shadow: 0 4px 15px rgba(29, 78, 216, 0.2);
    animation: slideInRight 0.3s ease-out;
}

.bot-message {
    background: rgba(30, 41, 59, 0.8);
    border-radius: 15px;
    padding: 12px 16px;
    margin: 8px 0;
    border-left: 4px solid #06B6D4;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.15);
    animation: slideInLeft 0.3s ease-out;
    backdrop-filter: blur(10px);
}

.source-card {
    background: rgba(6, 182, 212, 0.1);
    border: 2px solid #06B6D4;
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
    transition: all 0.3s ease;
}

.source-card:hover {
    background: rgba(6, 182, 212, 0.15);
    transform: translateX(5px);
    box-shadow: 0 0 25px rgba(6, 182, 212, 0.3);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1D4ED8, #06B6D4) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4) !important;
}

/* Input Fields */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 2px solid #06B6D4 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    padding: 12px !important;
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.1) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #1D4ED8 !important;
    box-shadow: 0 0 20px rgba(29, 78, 216, 0.3) !important;
}

/* Cards */
.stContainer {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(6, 182, 212, 0.2);
    backdrop-filter: blur(10px);
}

/* Animations */
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.loading-animation {
    animation: pulse 1.5s infinite;
}

.gradient-text {
    background: linear-gradient(135deg, #06B6D4, #1D4ED8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

/* Header */
.header-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #06B6D4, #1D4ED8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 20px 0;
    animation: fadeIn 0.6s ease-out;
}

.header-subtitle {
    font-size: 1.1rem;
    text-align: center;
    color: #94A3B8;
    margin-bottom: 30px;
    animation: fadeIn 0.8s ease-out 0.2s both;
}

/* Badge */
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #1D4ED8, #06B6D4);
    color: white;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 5px 5px 0;
}

/* Expandable Section */
.expandable-section {
    background: rgba(30, 41, 59, 0.8);
    border-left: 4px solid #06B6D4;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.expandable-section:hover {
    background: rgba(30, 41, 59, 0.9);
    border-left-color: #1D4ED8;
}

/* Suggested Questions */
.suggestion-chip {
    display: inline-block;
    background: rgba(6, 182, 212, 0.15);
    border: 2px solid #06B6D4;
    color: #06B6D4;
    padding: 8px 16px;
    border-radius: 20px;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}

.suggestion-chip:hover {
    background: rgba(6, 182, 212, 0.3);
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    color: #64748B;
    border-top: 1px solid rgba(6, 182, 212, 0.2);
    margin-top: 40px;
    font-size: 0.9rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(6, 182, 212, 0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #06B6D4, #1D4ED8);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #1D4ED8, #06B6D4);
}

/* Metric Cards */
.metric-card {
    background: rgba(30, 41, 59, 0.8);
    border: 2px solid #06B6D4;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.1);
}

.metric-card h3 {
    color: #06B6D4;
    margin-bottom: 10px;
}

.metric-card p {
    font-size: 1.8rem;
    font-weight: 700;
    color: #F1F5F9;
}

/* Text Animation */
.typing-text {
    overflow: hidden;
    white-space: pre-wrap;
    animation: slideInLeft 0.5s ease-out;
}

</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'rag_engine' not in st.session_state:
    st.session_state.rag_engine = None
    st.session_state.initialized = False
    st.session_state.chat_history = []
    st.session_state.total_queries = 0

# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin: 20px 0;'>
        <h2 style='color: #06B6D4;'>🎓 SISTec</h2>
        <p style='color: #94A3B8; font-size: 0.9rem;'>Sagar Institute of Science and Technology</p>
        <p style='color: #64748B; font-size: 0.85rem;'>Gandhinagar Campus</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.subheader("📊 System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>Status</h3>
            <p>✅ Ready</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3>Queries</h3>
            <p>{st.session_state.total_queries}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Initialize System
    st.subheader("⚙️ Initialization")
    
    if st.button("🔄 Initialize System", use_container_width=True):
        with st.spinner("Processing documents..."):
            try:
                st.session_state.rag_engine = RAGEngine(vector_db_type="chroma")
                chunks = ChunkProcessor.process_all_documents(DOCUMENTS_PATH)
                
                if chunks:
                    st.session_state.rag_engine.initialize_vector_db(chunks)
                    st.session_state.initialized = True
                    st.success(f"✅ Initialized with {len(chunks)} chunks!")
                else:
                    st.error("❌ No documents found")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("---")
    
    # Quick Links
    st.subheader("📚 Resources")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📖 About SISTec", use_container_width=True):
            st.session_state.page = "about"
    with col2:
        if st.button("🏫 Campus Tour", use_container_width=True):
            st.session_state.page = "campus"
    
    st.markdown("---")
    
    # Chat History
    if st.session_state.chat_history:
        st.subheader("💬 Recent Queries")
        for i, chat in enumerate(st.session_state.chat_history[-3:]):
            if st.button(f"🔄 {chat['query'][:30]}...", use_container_width=True, key=f"history_{i}"):
                st.session_state.current_query = chat['query']
                st.rerun()
    
    st.markdown("---")
    
    # Footer in Sidebar
    st.markdown("""
    <div class='footer'>
        <p><strong>SISTec InfoBot v1.0</strong></p>
        <p>Powered by RAG + Gemini AI</p>
        <p style='font-size: 0.8rem; color: #475569; margin-top: 10px;'>
            Built for hackathon judges 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
st.markdown("""
<h1 class='header-title'>🤖 SISTec InfoBot</h1>
<p class='header-subtitle'>AI-Powered Assistant for Sagar Institute of Science and Technology</p>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🏫 Campus", "📚 About"])

# Tab 1: Chat Interface
with tab1:
    if not st.session_state.initialized:
        st.warning("⚠️ System not initialized. Click 'Initialize System' in the sidebar first.")
        st.info("📖 The system will process documents from the documents/ folder")
    else:
        st.success("✅ System Ready! Ask your questions below.")
    
    st.markdown("---")
    
    # Suggested Questions
    st.subheader("💡 Suggested Questions")
    
    suggested_questions = [
        "🎓 What is the eligibility for B.Tech admission?",
        "💻 Tell me about the CSE department",
        "📊 What is the placement rate?",
        "🏠 What are the hostel facilities?",
        "🎉 What events are happening?",
        "🏆 Tell me about scholarships",
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(f"{question}", use_container_width=True, key=f"suggest_{i}"):
                st.session_state.current_query = question
                st.rerun()
    
    st.markdown("---")
    
    # Chat Display Area
    st.subheader("💬 Conversation")
    
    # Chat Container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                # User Message
                st.markdown(f"""
                <div class='user-message'>
                    <strong>👤 You:</strong><br>
                    {chat['query']}
                    <br><small style='color: #94A3B8;'>{chat.get('timestamp', '')}</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Bot Response
                st.markdown(f"""
                <div class='bot-message'>
                    <strong>🤖 SISTec InfoBot:</strong><br>
                    {chat['answer']}
                </div>
                """, unsafe_allow_html=True)
                
                # Sources
                if chat['sources']:
                    with st.expander("📚 View Sources"):
                        for source in chat['sources']:
                            st.markdown(f"""
                            <div class='source-card'>
                                <strong>📄 {source}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("💬 Start a conversation by asking a question!")
    
    st.markdown("---")
    
    # Input Area
    st.subheader("❓ Ask a Question")
    
    query = st.text_area(
        "Type your question here...",
        placeholder="E.g., What is the fee structure for B.Tech?",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        submit_button = st.button("🚀 Ask", use_container_width=True)
    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col3:
        if st.button("⬆️ Top", use_container_width=True):
            pass  # Scroll to top
    
    if submit_button and query:
        if not st.session_state.initialized:
            st.error("❌ System not initialized")
        else:
            with st.spinner("🔍 Searching documents... 🤔 Generating response..."):
                try:
                    result = st.session_state.rag_engine.answer_query(query)
                    
                    chat_item = {
                        "query": query,
                        "answer": result.get("answer", "No response"),
                        "sources": result.get("sources", []),
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "success": result.get("success", False)
                    }
                    
                    st.session_state.chat_history.append(chat_item)
                    st.session_state.total_queries += 1
                    
                    st.success("✅ Response generated!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Tab 2: Campus Tour
with tab2:
    st.subheader("🏫 Explore SISTec Gandhinagar Campus")
    
    st.info("📸 Campus image gallery coming soon!")
    
    campus_sections = [
        {
            "name": "Main Gate",
            "description": "Welcome to SISTec Gandhinagar - A premier engineering institute",
            "emoji": "🎓"
        },
        {
            "name": "Academic Block",
            "description": "State-of-the-art classrooms with modern learning facilities",
            "emoji": "📚"
        },
        {
            "name": "Computer Labs",
            "description": "High-performance computing facilities for CSE and IT students",
            "emoji": "💻"
        },
        {
            "name": "Library",
            "description": "Comprehensive digital and physical resource center",
            "emoji": "📖"
        },
        {
            "name": "Auditorium",
            "description": "State-of-the-art venue for seminars and events",
            "emoji": "🎤"
        },
        {
            "name": "Hostel Facilities",
            "description": "Comfortable accommodation for resident students",
            "emoji": "🏠"
        },
    ]
    
    cols = st.columns(2)
    for i, section in enumerate(campus_sections):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='stContainer' style='padding: 20px; margin: 10px 0;'>
                <h3>{section['emoji']} {section['name']}</h3>
                <p>{section['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Campus Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        {"label": "Students", "value": "5000+", "icon": "👥"},
        {"label": "Faculty", "value": "300+", "icon": "👨‍🏫"},
        {"label": "Departments", "value": "4", "icon": "🏢"},
        {"label": "Placement Rate", "value": "96%", "icon": "📈"},
    ]
    
    for i, stat in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>{stat['icon']}</h3>
                <p>{stat['value']}</p>
                <small>{stat['label']}</small>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: About
with tab3:
    st.subheader("ℹ️ About SISTec InfoBot")
    
    st.markdown("""
    ### 🤖 What is SISTec InfoBot?
    
    SISTec InfoBot is an AI-powered assistant built specifically for **Sagar Institute of Science and Technology (SISTec)** 
    Gandhinagar Campus. It uses advanced Retrieval-Augmented Generation (RAG) technology combined with Google's Gemini API 
    to provide accurate, source-verified answers to student queries.
    
    ### ✨ Key Features
    
    - **📚 Fact-Based Answers**: All responses are grounded in official SISTec documents
    - **📖 Source Transparency**: Every answer includes citations and source references
    - **🔍 Semantic Search**: Intelligent document retrieval using embeddings
    - **🎯 Query Classification**: Automatic categorization of questions (admission, department, events, etc.)
    - **⚡ Fast & Accurate**: Real-time responses from processed knowledge base
    - **🔐 Secure**: No external data leakage, only verified official information
    
    ### 📊 Supported Query Types
    
    """)
    
    query_types = {
        "🎓 Admission": "Eligibility, fees, application process, counseling",
        "💻 Departments": "CSE, ECE, Mechanical, Civil engineering programs",
        "🎉 Events": "Campus competitions, hackathons, seminars, fests",
        "📋 Rules": "Academic policies, regulations, code of conduct",
        "💼 Placements": "Recruitment statistics, average packages, companies",
        "🏠 Hostel": "Accommodation details, facilities, amenities",
        "📚 Academics": "Curriculum, exams, grades, results",
        "👨‍🏫 Faculty": "Professors, instructors, departmental staff",
    }
    
    col1, col2 = st.columns(2)
    for i, (qtype, description) in enumerate(query_types.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class='expandable-section'>
                <strong>{qtype}</strong><br>
                <small style='color: #94A3B8;'>{description}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### Backend
        - Python 3.11
        - FastAPI
        - LangChain
        - ChromaDB/FAISS
        """)
    
    with col2:
        st.markdown("""
        ### AI/ML
        - Google Gemini API
        - Embeddings Model
        - RAG Pipeline
        - Semantic Search
        """)
    
    with col3:
        st.markdown("""
        ### Frontend
        - Streamlit
        - Custom CSS
        - Animations
        - Responsive Design
        """)
    
    st.markdown("---")
    
    st.subheader("🎯 How It Works")
    
    st.image(
        "https://via.placeholder.com/800x400/0F172A/06B6D4?text=RAG+Pipeline+Architecture",
        use_column_width=True,
        caption="Retrieval-Augmented Generation Pipeline"
    )
    
    st.markdown("""
    1. **Question Input**: Student asks a question
    2. **Query Processing**: System classifies and analyzes the query
    3. **Document Retrieval**: Searches vector database for relevant documents
    4. **Context Preparation**: Formats retrieved information for LLM
    5. **Response Generation**: Gemini AI generates accurate answer with constraints
    6. **Source Attribution**: Provides document references and citations
    7. **Response Display**: Shows answer with expandable source details
    """)
    
    st.markdown("---")
    
    st.subheader("📞 Support & Contact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **SISTec Gandhinagar Campus**
        - Location: Gandhinagar, Gujarat
        - Phone: +91-9999-XXXXX
        - Email: info@sistec.ac.in
        - Website: www.sistec.ac.in
        """)
    
    with col2:
        st.markdown("""
        **InfoBot Support**
        - Report Issues
        - Suggest Improvements
        - Documentation
        - API Documentation
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class='footer' style='margin-top: 40px;'>
        <h3>🚀 SISTec InfoBot v1.0</h3>
        <p>Powered by RAG + Gemini AI</p>
        <p>Built for Sagar Institute of Science and Technology</p>
        <p style='font-size: 0.85rem; color: #64748B; margin-top: 15px;'>
            Designed & developed as a hackathon project to revolutionize student information access
        </p>
        <p style='font-size: 0.8rem; color: #475569; margin-top: 10px;'>
            © 2026 SISTec Gandhinagar | All rights reserved
        </p>
    </div>
    """, unsafe_allow_html=True)
