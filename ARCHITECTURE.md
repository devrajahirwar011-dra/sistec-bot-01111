# 🏗️ System Architecture - SISTec RAG Chatbot

## Overview

The SISTec RAG Chatbot is a retrieval-augmented generation system designed to provide accurate, source-verified answers about Sagar Institute of Science and Technology.

## Architecture Diagram

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
    ┌────▼─────────────┐
    │ Query Classifier │ ◄─── Identifies query type
    └────┬─────────────┘
         │
    ┌────▼──────────────────┐
    │ Out-of-Scope Check?   │
    └────┬──────────────────┘
         │
    ┌────▼─────────────────────────┐
    │ Vector Database Search        │ ◄─── Retrieves relevant chunks
    │ (Chroma/FAISS)               │
    └────┬─────────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Context Formatter         │ ◄─── Extracts sources
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Gemini API (with RAG)     │ ◄─── Generate answer
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Response Formatter        │ ◄─── Adds citations
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────┐
    │ User Response         │
    │ + Sources Citation    │
    └───────────────────────┘
```

## Components

### 1. **Document Processor** (`document_processor.py`)
Responsible for ingesting and preparing documents.

**Functions:**
- Extract text from PDF, DOCX, TXT files
- Chunk documents semantically (overlap preservation)
- Maintain metadata (filename, page number, section)

**Output:** Semantic chunks with metadata

### 2. **Vector Database** (`vector_db.py`)
Manages embeddings and similarity search.

**Implementations:**
- **Chroma**: Easy to use, good for small-medium databases
- **FAISS**: Faster, better for large databases

**Operations:**
- Store embeddings with metadata
- Perform semantic search (top-k retrieval)
- Filter by similarity threshold

### 3. **RAG Engine** (`rag_engine.py`)
Core retrieval-augmented generation logic.

**Components:**
- Query Classifier: Identifies query type
- Out-of-scope Detector: Filters invalid queries
- Retriever: Gets relevant chunks
- Context Formatter: Prepares for LLM
- Response Generator: Uses Gemini API with constraints

**Key Feature:** Strict RAG constraints prevent hallucination

### 4. **API Interface** (`chatbot_api.py`)
FastAPI server for web integration.

**Endpoints:**
- `POST /initialize` - Initialize with documents
- `POST /query` - Answer single query
- `POST /batch-query` - Answer multiple queries
- `GET /health` - System health check
- `GET /docs` - API documentation

### 5. **CLI Interface** (`chatbot_cli.py`)
Interactive command-line interface.

**Features:**
- Real-time conversation
- Built-in commands (/help, /rules, /status)
- Source attribution
- User-friendly formatting

## Data Flow

### Query Processing Flow

```
Input Query
    ↓
Parse & Validate
    ↓
Classify Query Type
    ├─ Admission
    ├─ Department
    ├─ Event
    ├─ Rules
    ├─ Placement
    ├─ Hostel
    ├─ Academic
    ├─ Faculty
    └─ Out-of-Scope?
         │
    ┌────▼──────────────┐
    │ Is Out-of-Scope?  │
    └────┬──────────────┘
         │ (Yes) → Reject
         │ (No)  ↓
    ┌────▼──────────────────────┐
    │ Generate Query Embedding  │ ◄─── Google Embeddings API
    └────┬──────────────────────┘
         │
    ┌────▼────────────────────┐
    │ Search Vector DB        │ ◄─── Top-K retrieval
    │ (Return top-5 chunks)   │
    └────┬────────────────────┘
         │
    ┌────▼──────────────────┐
    │ Format Context        │ ◄─── Merge chunks + sources
    └────┬──────────────────┘
         │
    ┌────▼────────────────────────────┐
    │ Create RAG Prompt               │
    │ - System prompt (strict rules)  │
    │ - Query                         │
    │ - Retrieved context             │
    │ - Instructions                  │
    └────┬────────────────────────────┘
         │
    ┌────▼──────────────────────┐
    │ Call Gemini API           │ ◄─── Answer generation
    │ (with constraints)        │
    └────┬──────────────────────┘
         │
    ┌────▼──────────────────┐
    │ Format Response       │ ◄─── Add citations
    │ + Sources            │
    └────┬──────────────────┘
         │
    Output Response
```

## Document Ingestion Pipeline

```
Raw Documents
(PDF, DOCX, TXT)
    │
    ├─ Extract Text
    │  ├─ PDF → PyPDF2
    │  ├─ DOCX → python-docx
    │  └─ TXT → Plain read
    │
    ├─ Preserve Metadata
    │  ├─ Filename
    │  ├─ Page number
    │  └─ Section info
    │
    ├─ Semantic Chunking
    │  ├─ Split by paragraphs
    │  ├─ Maintain chunk size
    │  └─ Add overlap (30%)
    │
    ├─ Generate Embeddings
    │  └─ Google Embeddings API
    │
    └─ Store in Vector DB
       ├─ Chroma (.db files)
       └─ FAISS (index + metadata.json)
```

## Query Classification System

```
Input Query
    │
    ├─ Extract keywords
    │
    └─ Match against patterns:
       │
       ├─ ADMISSION keywords
       │  [eligibility, admission, apply, counsel, fee, intake]
       │
       ├─ DEPARTMENT keywords
       │  [cse, ece, mechanical, civil, department, branch]
       │
       ├─ EVENT keywords
       │  [event, competition, hackathon, seminar, conference]
       │
       ├─ RULES keywords
       │  [rule, regulation, policy, code of conduct]
       │
       ├─ PLACEMENT keywords
       │  [placement, internship, job, recruit, salary]
       │
       ├─ HOSTEL keywords
       │  [hostel, accommodation, dormitory, campus life]
       │
       ├─ ACADEMIC keywords
       │  [academic, result, exam, grade, curriculum]
       │
       └─ FACULTY keywords
          [faculty, professor, instructor, staff]

    └─ Output: Query Type
```

## RAG Constraint System

### System Prompt Structure

```
SYSTEMIC_PROMPT
├─ Identity (SISTec chatbot)
├─ Strict Rules
│  ├─ Answer ONLY from context
│  ├─ No hallucination
│  ├─ No invented data
│  ├─ Always cite sources
│  └─ Handle unavailable info gracefully
├─ Query Types (8 categories)
├─ Out-of-Scope Topics
└─ Response Format
```

### Answer Generation Constraints

1. **Context-Only Requirement**
   - All statements must come from retrieved chunks
   - No external knowledge
   - No inference beyond context

2. **Source Attribution**
   - Always cite document + page
   - Track chunk sources
   - Maintain metadata accuracy

3. **Fact Verification**
   - Verify against retrieved content
   - Distinguish certain vs. uncertain info
   - Flag conflicting information

4. **Hallucination Prevention**
   - Reject out-of-context queries
   - Use "I don't know" responses
   - Never invent missing data

## Embedding Strategy

### Google Embeddings Model
```
Text Input
    │
    ├─ Tokenization
    │
    ├─ Semantic Encoding
    │  └─ 768-dimensional vectors
    │
    └─ Normalized Vectors
       └─ Ready for similarity search
```

### Similarity Calculation

```
Query Embedding
    │
    ├─ Calculate L2 distance to document embeddings
    │
    ├─ Convert to similarity score (1 / (1 + distance))
    │
    ├─ Filter by threshold (0.3)
    │
    └─ Return top-K (5) results
```

## Performance Considerations

### Latency Optimization

| Component | Latency | Optimization |
|-----------|---------|--------------|
| Embedding | ~100ms | Batch requests |
| Search | ~10ms | Use FAISS for large DB |
| LLM Call | ~2-5s | Reduce TOP_K to 3 |
| Total | ~3s | Parallel where possible |

### Memory Usage

| Component | Memory | Notes |
|-----------|--------|-------|
| Chroma DB | 500MB-2GB | Depends on chunk count |
| FAISS Index | 100MB-500MB | More efficient |
| Model Cache | 1GB | Google API (external) |
| Python Runtime | 500MB | Base requirement |

### Scalability

- **Vertical**: Increase chunk size, reduce TOP_K
- **Horizontal**: Multiple API instances + load balancer
- **Database**: Switch to FAISS for >10K chunks

## Security Model

```
Request
    │
    ├─ Input Validation
    │  └─ Reject harmful queries
    │
    ├─ API Key Management
    │  └─ Environment variables only
    │
    ├─ Query Isolation
    │  └─ No cross-query contamination
    │
    ├─ Source Verification
    │  └─ Only from document store
    │
    └─ Output Sanitization
       └─ No credential leakage

Response
    └─ Verified, Safe, Sourced
```

## Error Handling

```
Exception
    │
    ├─ API Key Error
    │  └─ Return helpful message
    │
    ├─ No Documents
    │  └─ Request user to initialize
    │
    ├─ Query Error
    │  └─ Suggest clarification
    │
    ├─ Gemini API Error
    │  └─ Retry with backoff
    │
    └─ Vector DB Error
       └─ Fallback or reinitialize
```

## Configuration Management

```
config.py
├─ API Keys (from .env)
├─ Model Selection
├─ Database Type
├─ Chunk Parameters
├─ RAG Thresholds
├─ Query Classifications
└─ System Prompts
```

## Testing Strategy

```
Test Suite
├─ Unit Tests
│  ├─ Query Classification
│  ├─ Chunking
│  ├─ Embedding
│  └─ Source Attribution
├─ Integration Tests
│  ├─ End-to-end flow
│  ├─ API endpoints
│  └─ RAG constraints
└─ Performance Tests
   ├─ Latency
   ├─ Throughput
   └─ Memory usage
```

---

**Architecture Version**: 1.0  
**Last Updated**: May 2026
