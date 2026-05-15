"""
RAG Engine for SISTec Chatbot
Combines document retrieval with Gemini API for answer generation
"""
from typing import List, Dict, Tuple
import google.generativeai as genai
from config import (
    GEMINI_API_KEY, GEMINI_MODEL, SYSTEMIC_PROMPT, 
    TOP_K_CHUNKS, TEMPERATURE, QUERY_TYPES
)
from vector_db import VectorDBFactory


class QueryClassifier:
    """Classify incoming queries for routing"""
    
    @staticmethod
    def classify_query(query: str) -> str:
        """Classify query type based on keywords"""
        query_lower = query.lower()
        
        for query_type, keywords in QUERY_TYPES.items():
            if any(keyword in query_lower for keyword in keywords):
                return query_type
        
        return "general"
    
    @staticmethod
    def is_out_of_scope(query: str) -> bool:
        """Check if query is out of scope"""
        out_of_scope_keywords = [
            "politics", "movie", "game", "coding tutorial",
            "python tutorial", "javascript", "weather", "sports",
            "celebrity", "personal advice"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in out_of_scope_keywords)


class RAGEngine:
    """Retrieval-Augmented Generation Engine"""
    
    def __init__(self, vector_db_type: str = "chroma"):
        genai.configure(api_key=GEMINI_API_KEY)
        self.vector_db = VectorDBFactory.create(vector_db_type)
        self.classifier = QueryClassifier()
    
    def initialize_vector_db(self, chunks: List[Dict]):
        """Initialize vector database with document chunks"""
        if hasattr(self.vector_db, 'create_collection'):
            self.vector_db.create_collection()
        
        self.vector_db.add_documents(chunks)
        print("Vector database initialized with documents")
    
    def retrieve_context(self, query: str, top_k: int = TOP_K_CHUNKS) -> List[Dict]:
        """Retrieve relevant document chunks"""
        retrieved = self.vector_db.search(query, top_k)
        return sorted(retrieved, key=lambda x: x['similarity'], reverse=True)
    
    def format_context(self, retrieved_chunks: List[Dict]) -> Tuple[str, List[str]]:
        """Format retrieved chunks for LLM and extract sources"""
        context_parts = []
        sources = set()
        
        for i, chunk in enumerate(retrieved_chunks, 1):
            text = chunk['text']
            metadata = chunk['metadata']
            context_parts.append(f"[Chunk {i}]\n{text}\n")
            
            # Build source citation
            source = metadata.get('filename', 'Unknown')
            if metadata.get('page'):
                source += f" — Page {metadata['page']}"
            if metadata.get('section'):
                source += f" ({metadata['section']})"
            sources.add(source)
        
        return "\n".join(context_parts), list(sources)
    
    def generate_response(self, query: str, context: str, sources: List[str]) -> Dict:
        """Generate response using Gemini with strict RAG constraints"""
        
        # Construct prompt with strict instructions
        prompt = f"""{SYSTEMIC_PROMPT}

USER QUERY: {query}

RETRIEVED CONTEXT:
{context}

INSTRUCTIONS:
1. Answer ONLY using the retrieved context above
2. If the context doesn't contain the answer, respond: "I could not find verified information for this in the SISTec knowledge base."
3. Do NOT use general knowledge or make assumptions
4. Always cite the source document
5. Be accurate, concise, and student-friendly

Generate your response now:
"""
        
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=TEMPERATURE,
                    max_output_tokens=1000
                )
            )
            
            answer = response.text if response.text else "Unable to generate response"
            
            return {
                "success": True,
                "answer": answer,
                "sources": sources,
                "query_type": self.classifier.classify_query(query)
            }
        
        except Exception as e:
            return {
                "success": False,
                "answer": f"Error generating response: {str(e)}",
                "sources": sources,
                "error": str(e)
            }
    
    def answer_query(self, query: str) -> Dict:
        """Main method: Answer user query with RAG"""
        
        # Check if query is out of scope
        if self.classifier.is_out_of_scope(query):
            return {
                "success": False,
                "answer": "This chatbot is designed specifically for SISTec-related information and cannot answer unrelated queries.",
                "sources": [],
                "query_type": "out_of_scope"
            }
        
        # Retrieve context
        retrieved = self.retrieve_context(query)
        
        # If no relevant context found
        if not retrieved:
            return {
                "success": False,
                "answer": "I could not find verified information for this in the SISTec knowledge base.",
                "sources": [],
                "query_type": self.classifier.classify_query(query)
            }
        
        # Format context and extract sources
        context, sources = self.format_context(retrieved)
        
        # Generate response with strict RAG constraints
        response = self.generate_response(query, context, sources)
        
        return response
    
    def clarify_ambiguous_query(self, query: str) -> str:
        """Handle ambiguous queries by asking for clarification"""
        query_type = self.classifier.classify_query(query)
        
        if query_type == "department":
            return "Could you please specify which department or course you're asking about? (e.g., CSE, ECE, Mechanical, Civil)"
        elif query_type == "admission":
            return "Could you provide more details? Are you asking about: eligibility, application process, fees, or required documents?"
        elif query_type == "event":
            return "Could you specify which event or program you're interested in?"
        else:
            return "Could you provide more details about your question?"
