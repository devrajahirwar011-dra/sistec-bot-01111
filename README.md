# SISTec RAG Chatbot

🎓 Official information chatbot for Sagar Institute of Science and Technology (SISTec) powered by Retrieval-Augmented Generation (RAG).

## 🎯 Features

- **Fact-Based Answers**: Responds only with information from verified documents
- **Source Attribution**: Every answer includes document sources and page references
- **Multiple Document Formats**: Supports PDF, DOCX, TXT, and Markdown files
- **Semantic Search**: Uses embeddings for intelligent document retrieval
- **Query Classification**: Automatically categorizes queries (admission, department, event, etc.)
- **Strict Knowledge Rules**: Prevents hallucination and invented information
- **Dual Interface**: CLI for interactive use, FastAPI for integration
- **Multiple Vector DBs**: Supports both Chroma and FAISS

## 📋 Supported Query Types

| Type | Keywords |
|------|----------|
| **Admission** | eligibility, admission, apply, counsel, fee, intake |
| **Department** | cse, ece, mechanical, civil, department, branch |
| **Event** | event, competition, hackathon, seminar, conference |
| **Rules** | rule, regulation, policy, code of conduct |
| **Placement** | placement, internship, job, recruit, salary |
| **Hostel** | hostel, accommodation, dormitory, campus life |
| **Academic** | academic, result, exam, grade, curriculum |
| **Faculty** | faculty, professor, instructor, staff |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

```bash
# Clone or navigate to project
cd sistec-rag-chatbot

# Run setup
python setup.py

# Configure API key
# Edit .env and set GEMINI_API_KEY=your-key-here
```

### Usage

#### 1. Interactive CLI
```bash
python main.py --cli
```

Features:
- Real-time chatbot interaction
- Document search and retrieval
- Source citations
- Command support (`/help`, `/rules`, `/status`)

#### 2. FastAPI Server
```bash
python main.py --api --port 8000
```

API Endpoints:
- `POST /initialize` - Initialize with documents
- `POST /query` - Answer a single query
- `POST /batch-query` - Answer multiple queries
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

#### 3. Single Query
```bash
python main.py --query "What is the eligibility for B.Tech admission?"
```

#### 4. Database Initialization
```bash
python main.py --init ./documents --db-type chroma
```

## 📁 Project Structure

```
sistec-rag-chatbot/
├── config.py                 # Configuration and system prompts
├── document_processor.py      # PDF/DOCX/TXT processing & chunking
├── vector_db.py             # Chroma & FAISS implementations
├── rag_engine.py            # Core RAG logic & answer generation
├── chatbot_api.py           # FastAPI interface
├── chatbot_cli.py           # CLI interface
├── main.py                  # Entry point
├── setup.py                 # Setup script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── documents/               # Document storage
│   ├── prospectus_2025.txt
│   └── admission_brochure_2025.txt
└── vector_store/            # Vector database storage
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Google API
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-1.5-flash

# Vector Database
VECTOR_DB_TYPE=chroma              # chroma or faiss
VECTOR_DB_PATH=./vector_store

# Processing
DOCUMENTS_PATH=./documents
CHUNK_SIZE=1000
CHUNK_OVERLAP=100

# RAG
TOP_K_CHUNKS=5
SIMILARITY_THRESHOLD=0.3

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 🔍 Query Examples

```
User: "What are the eligibility criteria for B.Tech?"
Bot: [Retrieves from documents] Pages eligibility details from Prospectus

User: "Tell me about CSE department"
Bot: [Searches CSE-related content] Returns department info with source

User: "What is the placement rate?"
Bot: [Queries placement section] Returns verified placement statistics

User: "Random movie question"
Bot: "This chatbot is designed specifically for SISTec-related information..."
```

## 📚 System Rules

The chatbot strictly follows these rules:

✅ **DO**
- Answer ONLY from retrieved documents
- Always cite sources with document names and page numbers
- Clarify ambiguous queries
- Distinguish between verified and unavailable information
- Use simple, student-friendly language

❌ **DON'T**
- Hallucinate or invent information
- Guess missing data (fees, dates, contacts, etc.)
- Use general internet knowledge
- Answer out-of-scope queries
- Share confidential information

## 🔗 API Usage Example

### Initialize System
```bash
curl -X POST "http://localhost:8000/initialize" \
  -H "Content-Type: application/json" \
  -d '{"documents_path": "./documents"}'
```

### Query Chatbot
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the B.Tech fee structure?"}'
```

Response:
```json
{
  "query": "What is the B.Tech fee structure?",
  "answer": "According to the Prospectus 2025...",
  "sources": [
    "prospectus_2025.txt — Page 5"
  ],
  "query_type": "admission",
  "success": true
}
```

### Batch Query
```bash
curl -X POST "http://localhost:8000/batch-query" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      {"query": "What are the departments?"},
      {"query": "What is the placement rate?"}
    ]
  }'
```

## 📊 Architecture

```
User Query
    ↓
[Query Classifier] → Out of scope?
    ↓ (No)
[Vector DB Search] → Retrieve relevant chunks
    ↓
[Context Formatter] → Prepare for LLM
    ↓
[Gemini API] → Generate answer with RAG constraints
    ↓
[Response Formatter] → Add sources & metadata
    ↓
User Response with Sources
```

## 🛠️ Adding New Documents

1. Place documents in `./documents/` folder
2. Supported formats: `.pdf`, `.docx`, `.txt`, `.md`
3. Run initialization:
   ```bash
   python main.py --init ./documents
   ```
4. Chatbot will automatically chunk and embed documents

## 📈 Performance Tuning

### For Speed
- Reduce `CHUNK_SIZE` to 500
- Reduce `TOP_K_CHUNKS` to 3
- Use FAISS (faster than Chroma for large databases)

### For Accuracy
- Increase `CHUNK_SIZE` to 1500
- Increase `TOP_K_CHUNKS` to 7
- Lower `SIMILARITY_THRESHOLD` to 0.2

### For Cost
- Use `gemini-1.5-flash` (faster, cheaper)
- Reduce `TOP_K_CHUNKS`
- Batch queries using `/batch-query`

## 🐛 Troubleshooting

### "Module not found" Error
```bash
python -m pip install -r requirements.txt
```

### Vector DB Connection Error
```bash
# Reset database
rm -rf ./vector_store
python main.py --init ./documents
```

### Gemini API Errors
- Verify `GEMINI_API_KEY` in `.env`
- Check API quota at [Google AI Console](https://ai.google.dev/)
- Rate limiting? Reduce concurrent requests

### Poor Answer Quality
- Add more relevant documents
- Check document chunking: `CHUNK_SIZE=1000`
- Verify `SIMILARITY_THRESHOLD=0.3`

## 📝 Logging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Logs saved to `./logs/`

## 🔐 Security

- No external data is leaked
- API keys stored in `.env` (never in code)
- Source documents not exposed (only chunks)
- Input validation on all endpoints

## 📦 Dependencies

- **google-generativeai**: Gemini API integration
- **langchain**: Text processing
- **chromadb**: Vector database
- **faiss-cpu**: Alternative vector DB
- **FastAPI**: Web framework
- **PyPDF2**: PDF processing
- **python-docx**: DOCX processing

## 🤝 Contributing

To improve the chatbot:

1. Add more documents to `./documents/`
2. Optimize chunking in `document_processor.py`
3. Fine-tune prompts in `config.py`
4. Add query examples for better classification

## 📞 Support

**Issues?**
- Check `.env` configuration
- Verify documents in `./documents/`
- Run `python setup.py` again
- Check logs in `./logs/`

## 📄 License

This project is designed for SISTec official use.

## 🎓 About SISTec

**Sagar Institute of Science and Technology**
- Location: MHOW, Indore, Madhya Pradesh
- NAAC A+ Grade
- Affiliated to RGPV, Bhopal
- Official Website: www.sistec.ac.in

---

**Last Updated**: May 2026
**Version**: 1.0.0
