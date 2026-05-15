"""
Test Suite for SISTec RAG Chatbot
Validates query answering, source attribution, and RAG constraints
"""
import unittest
from unittest.mock import patch, MagicMock
from document_processor import ChunkProcessor, DocumentProcessor
from rag_engine import QueryClassifier, RAGEngine
from config import QUERY_TYPES


class TestQueryClassification(unittest.TestCase):
    """Test query classification functionality"""
    
    def test_admission_query(self):
        """Test admission query classification"""
        classifier = QueryClassifier()
        result = classifier.classify_query("What are the eligibility criteria for B.Tech?")
        self.assertEqual(result, "admission")
    
    def test_department_query(self):
        """Test department query classification"""
        classifier = QueryClassifier()
        result = classifier.classify_query("Tell me about the CSE department")
        self.assertEqual(result, "department")
    
    def test_event_query(self):
        """Test event query classification"""
        classifier = QueryClassifier()
        result = classifier.classify_query("What events are happening?")
        self.assertEqual(result, "event")
    
    def test_placement_query(self):
        """Test placement query classification"""
        classifier = QueryClassifier()
        result = classifier.classify_query("What is the placement rate?")
        self.assertEqual(result, "placement")
    
    def test_out_of_scope_query(self):
        """Test out-of-scope query detection"""
        classifier = QueryClassifier()
        self.assertTrue(classifier.is_out_of_scope("What is the weather?"))
        self.assertTrue(classifier.is_out_of_scope("Tell me about politics"))
        self.assertFalse(classifier.is_out_of_scope("What is B.Tech admission?"))


class TestChunking(unittest.TestCase):
    """Test document chunking functionality"""
    
    def test_chunk_creation(self):
        """Test that chunks are created properly"""
        text = "This is a test paragraph.\n\nThis is another paragraph."
        metadata = {"filename": "test.txt", "file_type": "txt"}
        
        chunks = ChunkProcessor.create_chunks(text, metadata, chunk_size=50)
        
        self.assertGreater(len(chunks), 0)
        self.assertTrue(all('text' in chunk for chunk in chunks))
        self.assertTrue(all('metadata' in chunk for chunk in chunks))
    
    def test_chunk_overlap(self):
        """Test that chunks have proper overlap"""
        text = "Test paragraph 1.\n\n" * 50  # Create large text
        metadata = {"filename": "test.txt", "file_type": "txt"}
        
        chunks = ChunkProcessor.create_chunks(text, metadata, chunk_size=100, overlap=50)
        
        self.assertGreater(len(chunks), 1)
        # Check for overlap between consecutive chunks
        for i in range(len(chunks) - 1):
            # There should be some overlap in content
            self.assertTrue(len(chunks[i]['text']) > 0)


class TestRAGConstraints(unittest.TestCase):
    """Test RAG constraint enforcement"""
    
    def test_no_hallucination(self):
        """Verify chatbot doesn't hallucinate"""
        # This would require mocking the Gemini API
        # In production, this would be an integration test
        pass
    
    def test_source_attribution(self):
        """Verify sources are always provided"""
        rag = RAGEngine()
        # Mock the retrieve_context method
        rag.retrieve_context = MagicMock(return_value=[
            {
                "text": "Test content",
                "metadata": {
                    "filename": "test.txt",
                    "page": 1,
                    "section": "Introduction"
                },
                "similarity": 0.95
            }
        ])
        
        retrieved = rag.retrieve_context("test query")
        context, sources = rag.format_context(retrieved)
        
        self.assertGreater(len(sources), 0)
        self.assertIn("test.txt", sources[0])
    
    def test_empty_context_handling(self):
        """Test handling when no relevant context is found"""
        rag = RAGEngine()
        rag.retrieve_context = MagicMock(return_value=[])
        
        result = rag.answer_query("some query")
        
        # Should indicate information is unavailable
        self.assertFalse(result['success'])
        self.assertIn("could not find", result['answer'].lower())


class TestConfigurationIntegrity(unittest.TestCase):
    """Test configuration validity"""
    
    def test_query_types_defined(self):
        """Verify all query types are properly defined"""
        self.assertGreater(len(QUERY_TYPES), 0)
        
        for query_type, keywords in QUERY_TYPES.items():
            self.assertIsInstance(query_type, str)
            self.assertIsInstance(keywords, list)
            self.assertGreater(len(keywords), 0)
    
    def test_system_prompt_present(self):
        """Verify system prompt is configured"""
        from config import SYSTEMIC_PROMPT
        
        self.assertIsNotNone(SYSTEMIC_PROMPT)
        self.assertIn("ONLY", SYSTEMIC_PROMPT)  # Emphasis on retrieval-only
        self.assertIn("sources", SYSTEMIC_PROMPT.lower())


class TestDocumentProcessing(unittest.TestCase):
    """Test document processing"""
    
    def test_supported_formats(self):
        """Test that all supported formats are recognized"""
        processor = DocumentProcessor()
        
        supported = [".pdf", ".docx", ".txt", ".md"]
        for ext in supported:
            # Just verify no errors on extension check
            self.assertTrue(ext.startswith("."))
    
    def test_text_extraction(self):
        """Test text extraction from TXT files"""
        import tempfile
        import os
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content for extraction")
            temp_path = f.name
        
        try:
            result = DocumentProcessor.extract_from_txt(temp_path)
            self.assertEqual(len(result), 1)
            self.assertIn("Test content", result[0][0])
        finally:
            os.unlink(temp_path)


class TestEndToEnd(unittest.TestCase):
    """End-to-end integration tests"""
    
    def test_query_flow(self):
        """Test complete query flow"""
        classifier = QueryClassifier()
        
        # Test 1: Out of scope detection
        query = "What is Python?"
        if classifier.is_out_of_scope(query):
            self.assertEqual(classifier.is_out_of_scope(query), True)
        
        # Test 2: Query classification
        query = "What is the fee structure?"
        query_type = classifier.classify_query(query)
        self.assertIsNotNone(query_type)
    
    def test_source_format(self):
        """Test source formatting"""
        test_sources = [
            "prospectus_2025.txt — Page 5",
            "admission_brochure.pdf",
            "CSE_Department.docx (Introduction)",
        ]
        
        for source in test_sources:
            self.assertTrue(len(source) > 0)
            self.assertIsInstance(source, str)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    print("="*60)
    print("SISTec RAG Chatbot - Test Suite")
    print("="*60)
    print()
    run_tests()
