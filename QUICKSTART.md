"""
Quick start guide for RAG Q&A Support Bot

STEP 1: Environment Setup
========================
1. Create virtual environment:
   python -m venv venv
   
2. Activate it:
   Windows: venv\Scripts\activate
   Linux/Mac: source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt


STEP 2: Configuration
====================
1. Copy .env.example to .env:
   cp .env.example .env
   
2. Edit .env and set:
   - TARGET_WEBSITE=<your-website-url>
   - OPENAI_API_KEY (optional for future)
   - FLASK_PORT (default 5000)


STEP 3: Index Website Content
=============================
1. Run the indexing pipeline:
   python index_data.py
   
   This will:
   - Crawl the website
   - Clean and chunk content
   - Generate embeddings
   - Store in vector database


STEP 4: Start API Server
=======================
1. In a new terminal (with venv activated):
   python run_api.py
   
   Server will start at http://localhost:5000


STEP 5: Test the API
===================
Windows:
  test_api.bat

Linux/Mac:
  bash test_api.sh

Or use curl:
  curl http://localhost:5000/health
  curl http://localhost:5000/api/stats
  curl -X POST http://localhost:5000/api/ask \\
    -H "Content-Type: application/json" \\
    -d '{"question": "Your question?", "top_k": 5}'


TROUBLESHOOTING
===============
Q: ModuleNotFoundError: No module named 'src'
A: Run from project root directory

Q: Connection refused
A: Make sure Flask server is running (Step 4)

Q: No documents found
A: Run indexing first (Step 3)

Q: ImportError with dependencies
A: pip install -r requirements.txt

Q: Website not crawling
A: Check:
   - Internet connectivity
   - Website URL is correct and accessible
   - Website allows crawling (check robots.txt)


QUICK COMMANDS
==============
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# First run
copy .env.example .env
(Edit .env with your website URL)

# Index
python index_data.py

# Run
python run_api.py

# Test
test_api.bat (Windows) or bash test_api.sh (Linux/Mac)


For more detailed documentation, see README.md
"""