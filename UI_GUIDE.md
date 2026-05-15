# 🎨 SISTec InfoBot UI - User Guide

## 📱 Streamlit Web Interface

Modern, animated, college-themed AI chatbot interface for SISTec Gandhinagar Campus.

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Edit .env
GEMINI_API_KEY=your-api-key
```

### Step 3: Add Documents
Place documents in `documents/` folder (PDF, DOCX, TXT supported).

### Step 4: Run Streamlit App
```bash
streamlit run streamlit_app.py
```

The app will open at: **http://localhost:8501**

---

## 🎯 Interface Overview

### 📌 Main Components

#### 1. **Sidebar** (Left Panel)
- **SISTec Logo & Branding**
  - Institute name and campus info
  
- **System Status**
  - System health indicator
  - Query counter
  
- **Initialization Control**
  - Initialize System button
  - Processes all documents from `documents/` folder
  
- **Quick Links**
  - About SISTec
  - Campus Tour
  
- **Recent Queries**
  - History of recent questions
  - One-click re-query
  
- **Resources**
  - Footer with branding

#### 2. **Main Chat Tab** 💬
- **Header Section**
  - "SISTec InfoBot" title with gradient
  - Subtitle with animations
  
- **Suggested Questions**
  - 6 clickable question chips
  - Pre-formatted queries
  - Hover animations
  
- **Conversation Area**
  - User messages (right-aligned, blue gradient)
  - Bot messages (left-aligned, dark background)
  - Typing animations
  - Timestamps
  
- **Source Display**
  - Expandable source cards
  - Document references
  - Page numbers
  - Highlighted retrieved text
  
- **Input Area**
  - Large text area for questions
  - Ask button
  - Clear button
  - Scroll-to-top button

#### 3. **Campus Tour Tab** 🏫
- **Campus Sections**
  - Main Gate
  - Academic Block
  - Computer Labs
  - Library
  - Auditorium
  - Hostel Facilities
  
- **Campus Statistics**
  - Students
  - Faculty
  - Departments
  - Placement Rate

#### 4. **About Tab** 📚
- **InfoBot Introduction**
  - What is SISTec InfoBot
  
- **Key Features**
  - Fact-based answers
  - Source transparency
  - Semantic search
  - Query classification
  
- **Supported Query Types** (8 categories)
  - Admission
  - Departments
  - Events
  - Rules
  - Placements
  - Hostel
  - Academics
  - Faculty
  
- **Technology Stack**
  - Backend technologies
  - AI/ML components
  - Frontend framework
  
- **How It Works**
  - RAG Pipeline explanation
  - Step-by-step process
  
- **Support & Contact**
  - Campus information
  - Support channels

---

## 🎨 Design Features

### Color Palette
- **Primary Dark**: `#0F172A` (Deep Blue)
- **Primary Blue**: `#1D4ED8` (Royal Blue)
- **Accent Cyan**: `#06B6D4` (Cyan)
- **Background**: Gradient (Dark Navy to Black)
- **Text**: `#F1F5F9` (Light Gray)

### Animations
✨ **Smooth Fade-In Transitions**
- Header animations
- Message slide-in effects

✨ **Hover Effects**
- Button scaling
- Card elevation
- Source highlighting

✨ **Loading Animations**
- Pulse effect while generating
- Smooth transitions

✨ **Glassmorphism**
- Frosted glass effects
- Backdrop blur
- Semi-transparent overlays

### Typography
- **Bold, modern fonts**
- **Gradient text headings**
- **Clear, readable content**

---

## 💬 Chat Workflow

### Example: Asking a Question

```
1. Click "Suggested Questions" or type custom query
2. Click "🚀 Ask" button
3. Loading animation shows (thinking emoji)
4. Response appears with fade-in animation
5. Sources expandable below answer
6. Chat added to sidebar history
```

### Message Structure

**User Message:**
```
┌─────────────────────────────┐
│ 👤 You:                      │
│ Your question text          │
│ HH:MM:SS                    │
└─────────────────────────────┘
```

**Bot Message:**
```
┌─────────────────────────────┐
│ 🤖 SISTec InfoBot:           │
│ Response answer text        │
│ [📚 View Sources]           │
└─────────────────────────────┘
```

---

## 🔍 Features Explained

### Suggested Questions
Click any pre-formatted question to instantly get an answer:
- "🎓 What is the eligibility for B.Tech admission?"
- "💻 Tell me about the CSE department"
- "📊 What is the placement rate?"
- "🏠 What are the hostel facilities?"
- "🎉 What events are happening?"
- "🏆 Tell me about scholarships"

### Source Display
Expandable card showing:
- Document name
- Page number
- Retrieved text chunk
- Confidence indicator

Click "📚 View Sources" to expand/collapse source details.

### System Initialization
1. Click "🔄 Initialize System" in sidebar
2. System processes all documents
3. Creates embeddings using Google API
4. Stores in vector database
5. Shows success/error message

---

## ⚙️ Technical Details

### Session State Management
```python
st.session_state.rag_engine       # RAG instance
st.session_state.initialized      # Initialization flag
st.session_state.chat_history     # Conversation history
st.session_state.total_queries    # Query counter
```

### Custom CSS Classes
- `.user-message` - User message styling
- `.bot-message` - Bot message styling
- `.source-card` - Source display card
- `.suggestion-chip` - Question suggestion button
- `.gradient-text` - Gradient text effect
- `.loading-animation` - Pulse animation

### Integration Points
- **RAGEngine**: Answer generation
- **ChunkProcessor**: Document processing
- **Config**: System configuration
- **Vector DB**: Document retrieval

---

## 📊 Usage Statistics

The sidebar displays:
- **System Status**: ✅ Ready / ❌ Error
- **Query Count**: Total questions asked
- **Initialization Status**: Current state

---

## 🎯 Suggested Use Cases

### For Students
- "What is the eligibility for admission?"
- "Tell me about the CSE department"
- "When are placements happening?"
- "What are the hostel fees?"

### For Parents
- "What is the fee structure?"
- "What is the placement rate?"
- "Tell me about the campus facilities"
- "What scholarships are available?"

### For Judges
- "Show me source transparency" (click sources)
- "Demonstrate RAG capability" (ask technical questions)
- "Show system initialization" (click initialize)
- "Test batch queries" (ask multiple questions)

---

## 🐛 Troubleshooting

### Problem: "System not initialized"
**Solution**: Click "🔄 Initialize System" in sidebar first

### Problem: Empty chat history
**Solution**: Clear browser cache or reload the page

### Problem: Slow response times
**Solution**: 
- Reduce chunk size in config.py
- Use FAISS instead of Chroma
- Check internet connection

### Problem: API errors
**Solution**:
- Verify GEMINI_API_KEY in .env
- Check Google API quota
- Run `python setup.py` to reinstall

### Problem: No documents found
**Solution**:
- Ensure documents/ folder exists
- Add .pdf, .docx, or .txt files
- Run initialization again

---

## 🎨 Customization

### Change Colors
Edit the CSS in `streamlit_app.py`:
```python
--primary-blue: #1D4ED8;
--accent-cyan: #06B6D4;
```

### Add Campus Images
Replace placeholder in Campus Tour tab with actual images:
```python
st.image("path/to/campus.jpg", use_column_width=True)
```

### Modify Suggested Questions
Update the list in Chat tab:
```python
suggested_questions = [
    "Your question here",
    ...
]
```

### Change Theme Colors
Update custom CSS variables in `<style>` section

---

## 📱 Responsive Design

The interface works on:
- ✅ Desktop (1920x1080+)
- ✅ Tablet (iPad, Android)
- ✅ Mobile (with responsive layout)
- ✅ Wide screens (multiple columns)

---

## 🔒 Security Notes

✅ **What's Protected**
- API keys in environment variables
- No credential exposure
- Secure document storage
- Query isolation

✅ **What's Verified**
- All answers from documents only
- No external knowledge
- Source attribution
- Fact-checking enabled

---

## 📊 Performance Tips

1. **Faster Responses**
   - Reduce `TOP_K_CHUNKS` to 3
   - Use FAISS database
   - Cache frequent queries

2. **Better Accuracy**
   - Increase `CHUNK_SIZE` to 1500
   - Add more documents
   - Fine-tune prompts

3. **Improved UX**
   - Optimize images
   - Minimize animations on slow connections
   - Use CDN for assets

---

## 🚀 Deployment

### Local Streamlit
```bash
streamlit run streamlit_app.py
```

### Streamlit Cloud
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect GitHub repo
4. Deploy!

### Docker
```bash
docker build -f Dockerfile.streamlit -t sistec-ui .
docker run -p 8501:8501 sistec-ui
```

### Production
- Use Streamlit Server Certificate
- Enable authentication
- Add rate limiting
- Configure SSL/TLS

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Custom CSS Guide**: https://blog.streamlit.io/custom-components/
- **RAG Documentation**: See ARCHITECTURE.md
- **API Guide**: See api_client_examples.py

---

## 🎓 For Judges

### Demo Script

1. **Initialize** → Click "🔄 Initialize System"
2. **Ask Questions** → Click suggested questions or type custom
3. **Show Sources** → Click "📚 View Sources"
4. **Check Status** → View sidebar metrics
5. **Responsive Design** → Resize window to see mobile layout

### Talking Points
- ✨ Real-time RAG processing
- 🔍 Source transparency
- 🎨 Modern, animated UI
- 📱 Responsive design
- 🚀 Production-ready code
- 🔐 Secure, no hallucination
- 🎓 College-themed branding

---

**Version**: 1.0  
**Last Updated**: May 2026  
**Status**: ✅ Production Ready
