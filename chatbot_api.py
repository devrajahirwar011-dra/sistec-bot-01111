"""
FastAPI Chatbot Interface for SISTec RAG
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from rag_engine import RAGEngine
from document_processor import ChunkProcessor
import os

app = FastAPI(title="SISTec RAG Chatbot", version="1.0.0")

# RAG engine is created lazily to avoid heavy imports and import-time failures
rag_engine = None

# Flag to check if system is initialized
is_initialized = False


class QueryRequest(BaseModel):
    """Request body for chatbot query"""
    query: str
    top_k: Optional[int] = 5


class QueryResponse(BaseModel):
    """Response body from chatbot"""
    query: str
    answer: str
    sources: List[str]
    query_type: str
    success: bool


class InitializationRequest(BaseModel):
    """Request to initialize vector database"""
    documents_path: str = "./documents"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    initialized: bool
    vector_db_type: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "initialized": is_initialized,
        "vector_db_type": "chroma"
    }


@app.post("/initialize")
async def initialize_system(request: InitializationRequest):
    """Initialize vector database with documents"""
    global is_initialized, rag_engine

    try:
        if not os.path.exists(request.documents_path):
            raise HTTPException(
                status_code=400,
                detail=f"Documents path not found: {request.documents_path}"
            )

        # Lazily create RAG engine if not present
        if rag_engine is None:
            try:
                rag_engine = RAGEngine(vector_db_type="chroma")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create RAG engine: {e}")

        # Process all documents
        chunks = ChunkProcessor.process_all_documents(request.documents_path)

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No documents found to process"
            )

        # Initialize vector database
        rag_engine.initialize_vector_db(chunks)
        is_initialized = True

        return {
            "status": "initialized",
            "chunks_created": len(chunks),
            "documents_path": request.documents_path
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def answer_query(request: QueryRequest):
    """Answer user query using RAG"""
    
    if not is_initialized:
        raise HTTPException(
            status_code=400,
            detail="System not initialized. Please call /initialize first."
        )
    
    try:
        result = rag_engine.answer_query(request.query)
        
        return {
            "query": request.query,
            "answer": result["answer"],
            "sources": result["sources"],
            "query_type": result.get("query_type", "general"),
            "success": result["success"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/query-types")
async def get_query_types():
    """Get list of supported query types"""
    from config import QUERY_TYPES
    return {"query_types": QUERY_TYPES}


@app.get("/rules")
async def get_system_rules():
    """Get system behavior rules"""
    return {
        "rules": [
            "Answer ONLY from retrieved document context",
            "DO NOT hallucinate, guess, or use general internet knowledge",
            "DO NOT invent fees, dates, contacts, rankings, or placements",
            "ALWAYS cite sources with document names and page numbers",
            "If information unavailable, respond with verified information message",
            "Classify queries accurately (admission, department, event, etc.)",
            "Reject out-of-scope queries politely",
            "Handle ambiguous queries with clarification requests"
        ]
    }


@app.get("/system-prompt")
async def get_system_prompt():
    """Get current system prompt"""
    from config import SYSTEMIC_PROMPT
    return {"system_prompt": SYSTEMIC_PROMPT}


@app.post("/batch-query")
async def batch_query(requests: List[QueryRequest]):
    """Process multiple queries at once"""
    
    if not is_initialized:
        raise HTTPException(
            status_code=400,
            detail="System not initialized. Please call /initialize first."
        )
    
    results = []
    for request in requests:
        result = rag_engine.answer_query(request.query)
        results.append({
            "query": request.query,
            "answer": result["answer"],
            "sources": result["sources"],
            "success": result["success"]
        })
    
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
