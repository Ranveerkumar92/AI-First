# RAG Q&A Support Bot - Testing & Deployment Guide

## Table of Contents
1. [Unit Testing](#unit-testing)
2. [Integration Testing](#integration-testing)
3. [API Testing](#api-testing)
4. [Deployment](#deployment)
5. [Troubleshooting](#troubleshooting)

## Unit Testing

### Test the Crawler
```python
from src.crawler import WebCrawler

# Create crawler
crawler = WebCrawler("https://example.com", max_pages=5)

# Test URL validation
print(crawler.is_valid_url("https://example.com/page"))  # Should be True
print(crawler.is_valid_url("https://other.com/page"))    # Should be False

# Test HTML extraction
html = "<h1>Test</h1><p>Content</p>"
text = crawler.extract_text_from_html(html)
print(text)  # Should be "Test Content" or similar
```

### Test the Text Cleaner
```python
from src.cleaner import TextCleaner

# Test text cleaning
text = "   Multiple   spaces  and  special@#$  chars   "
cleaned = TextCleaner.clean_text(text)
print(cleaned)

# Test chunking
long_text = "This is a long text. " * 50
chunks = TextCleaner.chunk_text(long_text, chunk_size=200, overlap=50)
print(f"Created {len(chunks)} chunks")
```

### Test Embeddings
```python
from src.embeddings import EmbeddingsGenerator

gen = EmbeddingsGenerator()

# Single embedding
embedding = gen.generate_single_embedding("Hello world")
print(f"Embedding size: {len(embedding)}")  # Should be 384 for all-MiniLM-L6-v2

# Batch embeddings
texts = ["Hello", "Hi", "Good morning"]
embeddings = gen.generate_embeddings(texts)
print(f"Generated {len(embeddings)} embeddings")
```

### Test Vector Database
```python
from src.vector_db import VectorDatabase

# Initialize
db = VectorDatabase("./test_db")
db.create_collection()

# Add documents
docs = [
    {"id": "doc1", "content": "Hello world", "source": "test"},
    {"id": "doc2", "content": "Hi there", "source": "test"}
]
embeddings = [[0.1] * 384, [0.2] * 384]

db.add_documents(docs, embeddings)
db.persist()

# Search
results = db.search([0.15] * 384, n_results=2)
print(results)
```

## Integration Testing

### Full Pipeline Test
```python
from src.pipeline import IndexingPipeline
import os

# Mock test with simple HTML
os.environ['TARGET_WEBSITE'] = 'https://example.com'
pipeline = IndexingPipeline(
    website_url='https://example.com',
    max_pages=3
)
success = pipeline.run()
print("Pipeline success:", success)
```

## API Testing

### Using curl (Windows: cmd or PowerShell)

```bash
# 1. Test health endpoint
curl http://localhost:5000/health

# 2. Get statistics
curl http://localhost:5000/api/stats

# 3. Ask a question
curl -X POST http://localhost:5000/api/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is this about?\", \"top_k\": 3}"
```

### Using PowerShell
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5000/health" -Method Get

# Ask question
$body = @{
    question = "What services do you offer?"
    top_k = 5
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/ask" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

### Using Postman
1. Create GET request to `http://localhost:5000/health`
2. Create POST request to `http://localhost:5000/api/ask`
3. Set body to:
   ```json
   {
     "question": "Your question here?",
     "top_k": 5
   }
   ```

### Response Validation

**Expected Health Check Response:**
```json
{
  "status": "healthy",
  "service": "RAG Q&A Support Bot"
}
```

**Expected Ask Response:**
```json
{
  "question": "Your question",
  "retrieved_documents": [
    {
      "rank": 1,
      "content": "Document content...",
      "source": "https://example.com/page",
      "distance": 0.123
    }
  ],
  "total_results": 1,
  "status": "success"
}
```

## Deployment

### Local Development
```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Linux/Mac

# 2. Install
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your settings

# 4. Index
python index_data.py

# 5. Run
python run_api.py
```

### Production Deployment (with gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_api.py"]
```

Build and run:
```bash
docker build -t rag-qa-bot .
docker run -p 5000:5000 -e TARGET_WEBSITE=https://example.com rag-qa-bot
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'chromadb'"
**Solution:**
```bash
pip install chromadb --upgrade
```

### Issue: API returns no results
**Check:**
1. Database exists: `ls data/chroma_db/`
2. Run indexing: `python index_data.py`
3. Verify documents: `curl http://localhost:5000/api/stats`

### Issue: Crawling fails
**Check:**
1. Website is accessible: `curl https://example.com`
2. No firewall/proxy blocking
3. Website allows crawling (check robots.txt)

### Issue: Out of Memory
**Solutions:**
1. Reduce `max_pages` in `index_data.py`
2. Reduce chunk size
3. Use a smaller embedding model

### Issue: Slow Performance
**Optimization:**
1. Use `all-MiniLM-L6-v2` (already default)
2. Increase batch size
3. Use indexing server with more resources

## Performance Benchmarks

Typical performance (on mid-range machine):
- Crawling: 1-5 pages/sec
- Embedding generation: 50-100 texts/sec
- API response: 100-500ms for search

Database size estimates:
- Per document chunk: ~1KB text + 1.5KB embedding = ~2.5KB total
- 1000 chunks = ~2.5MB database

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test RAG Bot

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

## Monitoring

### Log Analysis
```bash
# View logs
tail -f app.log

# Filter for errors
grep ERROR app.log

# Count API calls
grep "POST /api/ask" app.log | wc -l
```

### Health Checks
Set up regular health checks:
```bash
*/5 * * * * curl -f http://localhost:5000/health || alert
```

---

For more information, see README.md and QUICKSTART.md
