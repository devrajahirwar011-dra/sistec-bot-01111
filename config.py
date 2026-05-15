"""
Configuration for SISTec RAG Chatbot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
GEMINI_MODEL = "gemini-1.5-flash"

# Vector Database Configuration
VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "chroma")  # chroma or faiss
VECTOR_DB_PATH = "./vector_store"
EMBEDDINGS_MODEL = "google-generativeai"  # Using Google's embeddings

# Document Configuration
DOCUMENTS_PATH = "./documents"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# RAG Configuration
TOP_K_CHUNKS = 5
SIMILARITY_THRESHOLD = 0.3

# Chatbot Configuration
MAX_RESPONSE_LENGTH = 1000
TEMPERATURE = 0.7

# System Instructions
SYSTEMIC_PROMPT = """You are an official SISTec (Sagar Institute of Science and Technology) information chatbot.

STRICT RULES:
1. ANSWER ONLY from retrieved document context
2. DO NOT hallucinate, guess, or use general internet knowledge
3. DO NOT invent fees, dates, contacts, rankings, or placements
4. ALWAYS cite sources with document names and page numbers
5. If information is unavailable, respond: "I could not find verified information for this in the SISTec knowledge base."

QUERY TYPES YOU HANDLE:
- Admission queries (eligibility, process, fees, documents)
- Department information
- Event details
- Academic rules and regulations
- Hostel information
- Placement information
- Faculty details
- General academic notices

OUT OF SCOPE:
- Politics, movies, unrelated coding
- General knowledge questions
- Personal advice unrelated to SISTec

RESPONSE FORMAT:
Answer: [Your response based on retrieved context]
Sources: [List documents with page/section]

Be concise, accurate, and student-friendly."""

# Supported Document Types
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".txt", ".md"]

# Query Classification
QUERY_TYPES = {
    "admission": ["eligibility", "admission", "apply", "counsel", "fee", "intake"],
    "department": ["cse", "ece", "mechanical", "civil", "department", "branch"],
    "event": ["event", "competition", "hackathon", "seminar", "conference"],
    "rules": ["rule", "regulation", "policy", "code of conduct"],
    "placement": ["placement", "internship", "job", "recruit", "salary"],
    "hostel": ["hostel", "accommodation", "dormitory", "campus life"],
    "academic": ["academic", "result", "exam", "grade", "curriculum"],
    "faculty": ["faculty", "professor", "instructor", "staff"],
}
