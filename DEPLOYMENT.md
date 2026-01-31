# Project Deployment Guide

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

#### 1. Clone Repository
```bash
git clone <repository-url>
cd AI-First
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings:
# - TARGET_WEBSITE: URL to crawl (e.g., https://docs.example.com)
# - VECTOR_DB_PATH: Path to store the vector database
# - FLASK_PORT: API port (default 5000)
# - OPENAI_API_KEY: (optional, for future OpenAI integration)
```

### First Run

#### Step 1: Index Website Content
```bash
python index_data.py
```
This will:
- Crawl the specified website
- Clean and chunk the content
- Generate embeddings
- Store in the vector database

Expected output: `Indexing Pipeline Completed Successfully!`

#### Step 2: Start the API Server
```bash
# In a new terminal window (with venv activated)
python run_api.py
```
The server will start at `http://localhost:5000`

#### Step 3: Test the API
```bash
# Windows
test_api.bat

# Linux/macOS
bash test_api.sh

# Or using curl
curl http://localhost:5000/health
```

## API Usage Examples

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

### Ask a Question
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What services do you offer?",
    "top_k": 5
  }'
```

## Project Structure

```
AI-First/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── api.py                   # Flask API endpoints
│   ├── crawler.py               # Web crawler
│   ├── cleaner.py               # Text cleaning
│   ├── embeddings.py            # Embedding generation
│   ├── vector_db.py             # Vector database interface
│   └── pipeline.py              # Indexing pipeline
├── data/                        # Data storage (gitignored)
├── index_data.py               # Indexing entry point
├── run_api.py                  # API server entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
├── QUICKSTART.md               # Quick start guide
├── TESTING.md                  # Testing guide
├── POSTMAN.md                  # Postman collection info
└── DEPLOYMENT.md              # This file
```

## Troubleshooting

### Virtual Environment Issues
```bash
# Reinstall venv
python -m venv venv --clear
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

### Port Already in Use
```bash
# Change port in .env
FLASK_PORT=5001

# Or kill process using port 5000
# Windows: netstat -ano | findstr :5000
# Linux/macOS: lsof -i :5000
```

### No Documents Retrieved
1. Verify indexing completed: `ls data/chroma_db/`
2. Re-run indexing: `python index_data.py`
3. Check API stats: `curl http://localhost:5000/api/stats`

### Slow Crawling/Indexing
- Reduce `max_pages` in `index_data.py`
- Use a faster internet connection
- Try a smaller website first

## Performance Optimization

### Recommended Settings

For different website sizes:

**Small sites (< 50 pages):**
```env
TARGET_WEBSITE=https://small-site.com
MAX_PAGES=50
CHUNK_SIZE=500
```

**Medium sites (50-500 pages):**
```env
TARGET_WEBSITE=https://medium-site.com
MAX_PAGES=100
CHUNK_SIZE=400
```

**Large sites (> 500 pages):**
```env
TARGET_WEBSITE=https://large-site.com
MAX_PAGES=200
CHUNK_SIZE=300
```

## Next Steps

1. **Test thoroughly** - Try different questions
2. **Monitor performance** - Watch for slow queries
3. **Backup data** - Keep copies of `data/chroma_db/`
4. **Scale up** - Add more documents/websites as needed
5. **Integrate** - Connect to other systems as needed

## Support

For issues:
1. Check QUICKSTART.md for common problems
2. Review TESTING.md for debugging
3. Check logs for error messages
4. Verify configuration in .env

## Maintenance

### Regular Tasks
- Monitor disk space usage
- Check API logs for errors
- Update indexed content periodically
- Backup vector database

### Database Maintenance
```python
# Clear old data if needed
from src.vector_db import VectorDatabase
db = VectorDatabase('./data/chroma_db')
# Implement cleanup logic as needed
```

## Security Considerations

1. **Environment Variables**: Keep `.env` secure, don't commit to git
2. **API Access**: Consider adding authentication for production
3. **Data Privacy**: Ensure compliance with data usage policies
4. **Rate Limiting**: Implement rate limiting for public APIs
5. **Input Validation**: All inputs are validated before processing

## Production Deployment

For production use, consider:

1. **Use Gunicorn/WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.api:app
   ```

2. **Use Docker**:
   ```bash
   docker build -t rag-qa-bot .
   docker run -p 5000:5000 rag-qa-bot
   ```

3. **Add Load Balancer**: Distribute requests across multiple instances

4. **Enable HTTPS**: Use SSL/TLS certificates

5. **Add Monitoring**: Set up logging and alerting

6. **Database Backup**: Regular backups of vector database

## Contact & Support

For questions or issues, refer to:
- README.md - Full documentation
- QUICKSTART.md - Quick start guide
- TESTING.md - Testing procedures
- POSTMAN.md - API testing with Postman
