"""
Main entry point for SISTec RAG Chatbot
Provides both CLI and API interfaces
"""
import argparse
import sys
from pathlib import Path


def main():
    """Main CLI handler"""
    parser = argparse.ArgumentParser(
        description="SISTec RAG Chatbot - Official Information System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --cli              # Start interactive CLI
  python main.py --api              # Start FastAPI server
  python main.py --init ./docs      # Initialize with documents
        """
    )
    
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Start interactive CLI interface"
    )
    
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start FastAPI server (default: localhost:8000)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for API server (default: 8000)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for API server (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--init",
        type=str,
        metavar="PATH",
        help="Initialize vector database with documents from PATH"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        metavar="QUERY",
        help="Single query mode - answer and exit"
    )
    
    parser.add_argument(
        "--db-type",
        choices=["chroma", "faiss"],
        default="chroma",
        help="Vector database type (default: chroma)"
    )
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if not any([args.cli, args.api, args.init, args.query]):
        print("SISTec RAG Chatbot\n")
        print("Choose an interface:")
        print("1. Interactive CLI:    python main.py --cli")
        print("2. FastAPI Server:     python main.py --api")
        print("3. Single Query:       python main.py --query \"Your question\"")
        print("\nFor full help: python main.py --help\n")
        return
    
    # CLI Mode
    if args.cli:
        from chatbot_cli import ChatbotCLI
        print("\n🚀 Starting SISTec Chatbot (CLI Mode)")
        cli = ChatbotCLI()
        cli.run()
    
    # API Mode
    if args.api:
        import uvicorn
        print(f"\n🚀 Starting SISTec Chatbot API on {args.host}:{args.port}")
        print(f"📚 Initialize: POST /initialize")
        print(f"💬 Query: POST /query")
        print(f"📖 API Docs: http://{args.host}:{args.port}/docs\n")
        uvicorn.run(
            "chatbot_api:app",
            host=args.host,
            port=args.port,
            reload=False
        )
    
    # Single Query Mode
    if args.query:
        from rag_engine import RAGEngine
        from document_processor import ChunkProcessor
        from config import DOCUMENTS_PATH
        
        print("\n🔄 Processing query...")
        
        try:
            # Initialize RAG engine
            rag_engine = RAGEngine(vector_db_type=args.db_type)
            
            # Process documents
            chunks = ChunkProcessor.process_all_documents(DOCUMENTS_PATH)
            if chunks:
                rag_engine.initialize_vector_db(chunks)
                
                # Get answer
                result = rag_engine.answer_query(args.query)
                
                print("\n" + "="*60)
                print("Answer:")
                print("="*60)
                print(result['answer'])
                
                if result['sources']:
                    print("\nSources:")
                    for source in result['sources']:
                        print(f"  • {source}")
                
                print("="*60 + "\n")
            else:
                print("❌ No documents found to process")
                sys.exit(1)
        
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    # Initialization Mode
    if args.init:
        from document_processor import ChunkProcessor
        from vector_db import VectorDBFactory
        
        print(f"\n🔄 Initializing with documents from: {args.init}")
        
        try:
            # Process documents
            chunks = ChunkProcessor.process_all_documents(args.init)
            
            if not chunks:
                print("❌ No documents found")
                sys.exit(1)
            
            # Initialize vector database
            vector_db = VectorDBFactory.create(args.db_type)
            if hasattr(vector_db, 'create_collection'):
                vector_db.create_collection()
            
            vector_db.add_documents(chunks)
            
            print(f"✅ Initialization complete!")
            print(f"   Database: {args.db_type}")
            print(f"   Chunks: {len(chunks)}")
            print(f"   Path: {args.init}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
