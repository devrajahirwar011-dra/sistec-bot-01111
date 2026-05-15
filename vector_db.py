"""
Vector Database Management for SISTec RAG Chatbot
Supports both Chroma and FAISS backends
"""
import os
import json
from typing import List, Dict, Tuple
import numpy as np
from config import VECTOR_DB_TYPE, VECTOR_DB_PATH, TOP_K_CHUNKS, SIMILARITY_THRESHOLD


class EmbeddingsProvider:
    """Generate embeddings using Google Gemini"""
    
    def __init__(self):
        try:
            import google.generativeai as genai
            from config import GEMINI_API_KEY
            genai.configure(api_key=GEMINI_API_KEY)
            self.genai = genai
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            self.genai = None
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for text using Google's model"""
        if not self.genai:
            return np.random.rand(768)  # Fallback random embedding
        
        try:
            result = self.genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            return np.array(result['embedding'])
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return np.random.rand(768)
    
    def embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for query"""
        if not self.genai:
            return np.random.rand(768)
        
        try:
            result = self.genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="RETRIEVAL_QUERY"
            )
            return np.array(result['embedding'])
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return np.random.rand(768)


class ChromaVectorDB:
    """Chroma vector database wrapper"""
    
    def __init__(self, persist_dir: str = VECTOR_DB_PATH):
        try:
            import chromadb
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = None
            self.embeddings = EmbeddingsProvider()
        except Exception as e:
            print(f"Error initializing Chroma: {e}")
    
    def create_collection(self, name: str = "sistec_documents"):
        """Create or get collection"""
        try:
            self.collection = self.client.get_or_create_collection(name=name)
            print(f"Chroma collection '{name}' ready")
        except Exception as e:
            print(f"Error creating collection: {e}")
    
    def add_documents(self, chunks: List[Dict]):
        """Add document chunks to Chroma"""
        if not self.collection:
            self.create_collection()
        
        try:
            for i, chunk in enumerate(chunks):
                embedding = self.embeddings.embed_text(chunk["text"])
                self.collection.add(
                    ids=[f"chunk_{i}"],
                    documents=[chunk["text"]],
                    metadatas=[chunk["metadata"]],
                    embeddings=[embedding.tolist()]
                )
            print(f"Added {len(chunks)} chunks to Chroma")
        except Exception as e:
            print(f"Error adding documents to Chroma: {e}")
    
    def search(self, query: str, top_k: int = TOP_K_CHUNKS) -> List[Dict]:
        """Search for relevant chunks"""
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            retrieved = []
            if results['documents'] and len(results['documents']) > 0:
                for doc, metadata, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                ):
                    # Chroma returns distances, convert to similarity score
                    similarity = 1 / (1 + distance)
                    if similarity >= SIMILARITY_THRESHOLD:
                        retrieved.append({
                            "text": doc,
                            "metadata": metadata,
                            "similarity": similarity
                        })
            
            return retrieved
        except Exception as e:
            print(f"Error searching Chroma: {e}")
            return []


class FAISSVectorDB:
    """FAISS vector database wrapper"""
    
    def __init__(self, persist_dir: str = VECTOR_DB_PATH):
        try:
            import faiss
            self.faiss = faiss
            self.persist_dir = persist_dir
            self.index = None
            self.embeddings = EmbeddingsProvider()
            self.chunks = []
            os.makedirs(persist_dir, exist_ok=True)
        except Exception as e:
            print(f"Error initializing FAISS: {e}")
    
    def create_index(self, dimension: int = 768):
        """Create FAISS index"""
        try:
            self.index = self.faiss.IndexFlatL2(dimension)
            print("FAISS index created")
        except Exception as e:
            print(f"Error creating FAISS index: {e}")
    
    def add_documents(self, chunks: List[Dict]):
        """Add document chunks to FAISS"""
        if not self.index:
            self.create_index()
        
        try:
            embeddings_list = []
            for chunk in chunks:
                embedding = self.embeddings.embed_text(chunk["text"])
                embeddings_list.append(embedding)
                self.chunks.append(chunk)
            
            embeddings_array = np.array(embeddings_list).astype('float32')
            self.index.add(embeddings_array)
            
            # Save metadata
            metadata_path = os.path.join(self.persist_dir, "metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(self.chunks, f)
            
            print(f"Added {len(chunks)} chunks to FAISS")
        except Exception as e:
            print(f"Error adding documents to FAISS: {e}")
    
    def search(self, query: str, top_k: int = TOP_K_CHUNKS) -> List[Dict]:
        """Search for relevant chunks"""
        if not self.index or len(self.chunks) == 0:
            return []
        
        try:
            query_embedding = self.embeddings.embed_query(query)
            query_array = np.array([query_embedding]).astype('float32')
            
            distances, indices = self.index.search(query_array, top_k)
            
            retrieved = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx < len(self.chunks):
                    # Convert L2 distance to similarity score
                    similarity = 1 / (1 + distance)
                    if similarity >= SIMILARITY_THRESHOLD:
                        chunk = self.chunks[int(idx)]
                        retrieved.append({
                            "text": chunk["text"],
                            "metadata": chunk["metadata"],
                            "similarity": similarity
                        })
            
            return retrieved
        except Exception as e:
            print(f"Error searching FAISS: {e}")
            return []


class VectorDBFactory:
    """Factory to create appropriate vector database"""
    
    @staticmethod
    def create(db_type: str = VECTOR_DB_TYPE, persist_dir: str = VECTOR_DB_PATH):
        """Create vector database instance"""
        if db_type.lower() == "chroma":
            return ChromaVectorDB(persist_dir)
        elif db_type.lower() == "faiss":
            return FAISSVectorDB(persist_dir)
        else:
            print(f"Unknown DB type: {db_type}, defaulting to Chroma")
            return ChromaVectorDB(persist_dir)
