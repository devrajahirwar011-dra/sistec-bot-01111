"""
Document Processor for SISTec RAG Chatbot
Handles PDF, DOCX, TXT files with chunking and metadata preservation
"""
import os
import re
from typing import List, Dict, Tuple
from pathlib import Path
import PyPDF2
from docx import Document as DocxDocument
from config import CHUNK_SIZE, CHUNK_OVERLAP, DOCUMENTS_PATH, SUPPORTED_EXTENSIONS


class DocumentMetadata:
    """Stores metadata for document chunks"""
    def __init__(self, filename: str, file_type: str, page: int = None, section: str = None):
        self.filename = filename
        self.file_type = file_type
        self.page = page
        self.section = section
    
    def to_dict(self):
        return {
            "filename": self.filename,
            "file_type": self.file_type,
            "page": self.page,
            "section": self.section
        }


class DocumentProcessor:
    """Process various document types and create semantic chunks"""
    
    @staticmethod
    def extract_from_pdf(file_path: str) -> List[Tuple[str, Dict]]:
        """Extract text from PDF with page tracking"""
        chunks = []
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    metadata = {
                        "filename": os.path.basename(file_path),
                        "file_type": "pdf",
                        "page": page_num,
                        "source": file_path
                    }
                    chunks.append((text, metadata))
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        
        return chunks
    
    @staticmethod
    def extract_from_docx(file_path: str) -> List[Tuple[str, Dict]]:
        """Extract text from DOCX with paragraph tracking"""
        chunks = []
        try:
            doc = DocxDocument(file_path)
            text_parts = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    text_parts.append(para.text)
            
            full_text = "\n".join(text_parts)
            metadata = {
                "filename": os.path.basename(file_path),
                "file_type": "docx",
                "page": None,
                "source": file_path
            }
            chunks.append((full_text, metadata))
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
        
        return chunks
    
    @staticmethod
    def extract_from_txt(file_path: str) -> List[Tuple[str, Dict]]:
        """Extract text from TXT file"""
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            metadata = {
                "filename": os.path.basename(file_path),
                "file_type": "txt",
                "page": None,
                "source": file_path
            }
            chunks.append((text, metadata))
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
        
        return chunks
    
    @staticmethod
    def extract_text(file_path: str) -> List[Tuple[str, Dict]]:
        """Route to appropriate extraction method"""
        ext = Path(file_path).suffix.lower()
        
        if ext == ".pdf":
            return DocumentProcessor.extract_from_pdf(file_path)
        elif ext == ".docx":
            return DocumentProcessor.extract_from_docx(file_path)
        elif ext in [".txt", ".md"]:
            return DocumentProcessor.extract_from_txt(file_path)
        else:
            print(f"Unsupported file type: {ext}")
            return []


class ChunkProcessor:
    """Handle semantic chunking with overlap"""
    
    @staticmethod
    def create_chunks(text: str, metadata: Dict, chunk_size: int = CHUNK_SIZE, 
                     overlap: int = CHUNK_OVERLAP) -> List[Dict]:
        """
        Create overlapping chunks from text while preserving semantic structure
        """
        chunks = []
        
        # Split by paragraphs first for better semantics
        paragraphs = text.split('\n\n')
        current_chunk = ""
        chunk_metadata = metadata.copy()
        
        for para in paragraphs:
            if not para.strip():
                continue
            
            # If adding paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": chunk_metadata
                })
                # Create overlap by keeping last 30% of text
                current_chunk = current_chunk[-int(chunk_size * 0.3):] + "\n" + para
            else:
                current_chunk += "\n" + para if current_chunk else para
        
        # Add remaining text
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": chunk_metadata
            })
        
        return chunks
    
    @staticmethod
    def process_all_documents(docs_path: str = DOCUMENTS_PATH) -> List[Dict]:
        """Process all supported documents in a directory"""
        all_chunks = []
        
        if not os.path.exists(docs_path):
            print(f"Documents directory not found: {docs_path}")
            return all_chunks
        
        for file in os.listdir(docs_path):
            if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                file_path = os.path.join(docs_path, file)
                print(f"Processing {file}...")
                
                # Extract text
                text_chunks = DocumentProcessor.extract_text(file_path)
                
                # Create semantic chunks
                for text, metadata in text_chunks:
                    semantic_chunks = ChunkProcessor.create_chunks(text, metadata)
                    all_chunks.extend(semantic_chunks)
        
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
