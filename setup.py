"""
Setup and Installation Script for SISTec RAG Chatbot
"""
import os
import sys
import subprocess
from pathlib import Path


def setup():
    """Run setup for the chatbot"""
    
    print("\n" + "="*60)
    print("🚀 SISTec RAG Chatbot Setup")
    print("="*60)
    
    # Check Python version
    print("\n1️⃣  Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create directories
    print("\n2️⃣  Creating directories...")
    dirs = [
        "./documents",
        "./vector_store",
        "./logs"
    ]
    for directory in dirs:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Install dependencies
    print("\n3️⃣  Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    print("\n4️⃣  Setting up environment...")
    if not os.path.exists(".env"):
        print("   Creating .env from template...")
        with open(".env.example", "r") as src:
            with open(".env", "w") as dst:
                dst.write(src.read())
        print("   ✅ .env created (EDIT THIS WITH YOUR API KEY!)")
    else:
        print("   ✅ .env already exists")
    
    # Display next steps
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\n📝 Next Steps:")
    print("\n1. Configure your API key:")
    print("   Edit .env and set GEMINI_API_KEY")
    print("\n2. Add your documents:")
    print("   Place PDF/DOCX/TXT files in ./documents/")
    print("\n3. Start the chatbot:")
    print("\n   Interactive CLI:")
    print("     python main.py --cli")
    print("\n   FastAPI Server:")
    print("     python main.py --api")
    print("\n   Single Query:")
    print("     python main.py --query \"Your question\"")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    setup()
