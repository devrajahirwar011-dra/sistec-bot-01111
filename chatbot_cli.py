"""
CLI Interface for SISTec RAG Chatbot
Standalone command-line tool for interacting with the chatbot
"""
import os
import sys
from pathlib import Path
from document_processor import ChunkProcessor
from rag_engine import RAGEngine
from config import DOCUMENTS_PATH


class ChatbotCLI:
    """Command-line interface for the chatbot"""
    
    def __init__(self):
        self.rag_engine = RAGEngine(vector_db_type="chroma")
        self.initialized = False
    
    def initialize(self, docs_path: str = DOCUMENTS_PATH):
        """Initialize the chatbot with documents"""
        print(f"\n🔄 Initializing chatbot from: {docs_path}")
        
        if not os.path.exists(docs_path):
            print(f"❌ Documents directory not found: {docs_path}")
            print(f"   Creating directory: {docs_path}")
            os.makedirs(docs_path)
            print(f"   Please add documents to {docs_path} and try again.")
            return False
        
        # Check for documents
        doc_files = [f for f in os.listdir(docs_path) 
                    if f.endswith(('.pdf', '.docx', '.txt', '.md'))]
        
        if not doc_files:
            print(f"⚠️  No documents found in {docs_path}")
            print("   Supported formats: .pdf, .docx, .txt, .md")
            return False
        
        print(f"📄 Found {len(doc_files)} document(s)")
        
        try:
            # Process all documents
            chunks = ChunkProcessor.process_all_documents(docs_path)
            
            if not chunks:
                print("❌ Failed to create chunks from documents")
                return False
            
            # Initialize RAG engine
            self.rag_engine.initialize_vector_db(chunks)
            self.initialized = True
            
            print(f"✅ Chatbot initialized successfully!")
            print(f"   Total chunks: {len(chunks)}")
            return True
        
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            return False
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🎓 Sagar Institute of Science and Technology (SISTec)")
        print("="*60)
        print("\nThis chatbot provides accurate, source-verified information")
        print("about SISTec admissions, academics, events, and more.")
        print("\nCommands:")
        print("  /help       - Show available commands")
        print("  /rules      - Show chatbot behavior rules")
        print("  /status     - Check system status")
        print("  /exit       - Exit the chatbot")
        print("\nType your question and press Enter:")
        print("-"*60 + "\n")
    
    def display_help(self):
        """Show help message"""
        print("\n" + "="*60)
        print("Commands:")
        print("="*60)
        print("/help       - Show this help message")
        print("/rules      - Display system rules and guidelines")
        print("/types      - Show supported query types")
        print("/status     - Check initialization status")
        print("/exit       - Exit the chatbot")
        print("\nQuery Examples:")
        print("  'What are the eligibility criteria for B.Tech?'")
        print("  'Tell me about CSE department'")
        print("  'What are the upcoming events?'")
        print("  'What is the placement process?'")
        print("="*60 + "\n")
    
    def display_rules(self):
        """Show system rules"""
        rules = [
            "✅ Answer ONLY from retrieved documents",
            "❌ NO hallucinations or general knowledge",
            "❌ NO invented fees, dates, or rankings",
            "📚 Always cite sources",
            "🤔 Clarify ambiguous questions",
            "🚫 Reject out-of-scope queries",
            "📋 Verify all factual claims"
        ]
        print("\n" + "="*60)
        print("System Rules:")
        print("="*60)
        for rule in rules:
            print(f"  {rule}")
        print("="*60 + "\n")
    
    def display_query_types(self):
        """Show supported query types"""
        from config import QUERY_TYPES
        print("\n" + "="*60)
        print("Supported Query Types:")
        print("="*60)
        for qtype, keywords in QUERY_TYPES.items():
            print(f"\n{qtype.upper()}")
            print(f"  Keywords: {', '.join(keywords[:5])}")
        print("="*60 + "\n")
    
    def display_status(self):
        """Show system status"""
        status = "✅ READY" if self.initialized else "❌ NOT INITIALIZED"
        print("\n" + "="*60)
        print("System Status")
        print("="*60)
        print(f"Status: {status}")
        print(f"Vector DB: Chroma")
        print(f"Model: Gemini")
        print("="*60 + "\n")
    
    def process_command(self, user_input: str):
        """Process special commands"""
        command = user_input.lower().strip()
        
        if command == "/help":
            self.display_help()
            return True
        elif command == "/rules":
            self.display_rules()
            return True
        elif command == "/types":
            self.display_query_types()
            return True
        elif command == "/status":
            self.display_status()
            return True
        elif command == "/exit":
            print("\n👋 Goodbye!\n")
            return False
        
        return None  # Not a command
    
    def format_response(self, response: dict):
        """Format and display response"""
        print("\n" + "="*60)
        print("💬 Answer")
        print("="*60)
        print(response['answer'])
        
        if response['sources']:
            print("\n📚 Sources:")
            for source in response['sources']:
                print(f"  • {source}")
        
        if not response['success']:
            print("\n⚠️  Note: This information could not be verified")
        
        print("="*60 + "\n")
    
    def run(self):
        """Main CLI loop"""
        # Initialize
        if not self.initialize():
            print("\n❌ Cannot start chatbot without documents")
            print(f"   Please add documents to: {DOCUMENTS_PATH}")
            return
        
        # Welcome
        self.display_welcome()
        
        # Main loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                is_command = self.process_command(user_input)
                if is_command is False:
                    break
                if is_command:
                    continue
                
                # Process query
                print("\n🔍 Searching documents...")
                response = self.rag_engine.answer_query(user_input)
                self.format_response(response)
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def main():
    """Main entry point"""
    cli = ChatbotCLI()
    cli.run()


if __name__ == "__main__":
    main()
