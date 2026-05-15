# ⚡ Quick Start Guide - SISTec RAG Chatbot

Get the chatbot running in 5 minutes!

## 🚀 Option 1: Local CLI (Easiest)

### Step 1: Setup
```bash
cd sistec-rag-chatbot
python setup.py
```

### Step 2: Configure API Key
```bash
# Edit .env file
notepad .env  # Windows
# or
nano .env     # Linux/Mac
```

Set `GEMINI_API_KEY=your-key-here`

### Step 3: Add Documents
Place your documents in `documents/` folder. Example files are already included.

### Step 4: Run
```bash
python main.py --cli
```

### Step 5: Ask Questions
```
You: What is the B.Tech fee structure?
Bot: [Answers with sources]

You: /help
Bot: [Shows available commands]

You: /exit
Bot: Goodbye!
```

---

## 🐳 Option 2: Docker (Recommended for Deployment)

### Step 1: Build
```bash
docker build -t sistec-chatbot .
```

### Step 2: Run
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your-key-here \
  -v $(pwd)/documents:/app/documents \
  sistec-chatbot
```

### Step 3: Test
```bash
curl http://localhost:8000/health
```

### Step 4: Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the eligibility?"}'
```

---

## 🌐 Option 3: API Server

### Step 1: Start
```bash
python main.py --api
```

### Step 2: Access Docs
Open browser: `http://localhost:8000/docs`

### Step 3: Try It Out
- Click "Initialize" → Execute
- Click "Query" → Try a question

---

## 📝 Sample Queries

Try these questions with the sample documents:

```
✅ "What is the eligibility for B.Tech?"
✅ "Tell me about the CSE department"
✅ "What is the fee structure?"
✅ "What is the placement rate?"
✅ "What are the hostel fees?"
✅ "What is the average package?"
✅ "How many seats are available?"
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
```bash
python -m pip install -r requirements.txt
```

### Problem: "No documents found"
- Create `documents/` folder
- Add `.pdf`, `.docx`, or `.txt` files
- Run initialization again

### Problem: "API Key not working"
- Check `.env` file for correct key
- Verify key is active on Google Cloud Console

### Problem: Slow responses
- Reduce `CHUNK_SIZE` in `.env` to 500
- Reduce `TOP_K_CHUNKS` to 3

---

## 📚 Add Your Documents

1. Create `documents/` folder
2. Add files:
   - Prospectus PDF
   - Admission brochure
   - Department info
   - Event schedules
   - Rulebooks
   - Any other relevant docs

3. Reinitialize:
```bash
python main.py --init ./documents
```

---

## 🎯 Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Review [api_client_examples.py](api_client_examples.py) for integration
- Run tests: `python test_chatbot.py`

---

## 💡 Common Commands

```bash
# Interactive CLI
python main.py --cli

# Start API server
python main.py --api --port 8000

# Single query
python main.py --query "Your question here"

# Initialize documents
python main.py --init ./documents

# Initialize with FAISS
python main.py --init ./documents --db-type faiss

# Run tests
python test_chatbot.py

# Show API examples
python api_client_examples.py basic
```

---

## 🔗 API Quick Reference

### Health Check
```bash
GET http://localhost:8000/health
```

### Initialize
```bash
POST http://localhost:8000/initialize
Body: {"documents_path": "./documents"}
```

### Query
```bash
POST http://localhost:8000/query
Body: {"query": "Your question", "top_k": 5}
```

### Batch Query
```bash
POST http://localhost:8000/batch-query
Body: {"requests": [{"query": "Q1"}, {"query": "Q2"}]}
```

---

## 📞 Support

Having issues? Check:
1. `.env` configuration is correct
2. Documents are in `documents/` folder
3. Google API key is valid
4. Run `setup.py` again

---

**Ready to go!** 🎉

Start with: `python main.py --cli`
