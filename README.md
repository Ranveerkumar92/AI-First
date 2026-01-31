# RAG Q&A Support Bot

A complete implementation of a Retrieval Augmented Generation (RAG) system for building intelligent Q&A support bots. This project crawls websites, generates embeddings, stores them in a vector database, and provides an API for answering questions based on the crawled content.

## Project Overview

This RAG pipeline includes:
1. **Web Crawler** - Extracts content from website pages
2. **Text Cleaner** - Cleans and chunks text for optimal embedding generation
3. **Embeddings Generator** - Creates vector embeddings using OpenAI's API
4. **Vector Database** - Stores and retrieves embeddings using Pinecone
5. **Q&A Engine** - Retrieves relevant context and generates answers using GPT

## Architecture

```
User Query
    ↓
[Query Embedding] ← OpenAI API
    ↓
[Vector Search] ← Pinecone DB
    ↓
[Context Retrieval]
    ↓
[Answer Generation] ← GPT-3.5-Turbo
    ↓
Answer + Sources
```

## Prerequisites

- Python 3.8+
- OpenAI API key (for embeddings and LLM)
- Pinecone API key (for vector storage)
- pip package manager

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd AI-First
```

2. **Create a Python virtual environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Copy the example config
cp .env.example .env

# Edit .env with your API keys
```

**Required environment variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_ENVIRONMENT` - Your Pinecone environment (e.g., "us-west1-gcp")
- `PINECONE_INDEX_NAME` - Name for your Pinecone index
- `TARGET_URL` - Website URL to crawl (optional)
- `FLASK_PORT` - Port for API server (default: 5000)

## Project Structure

```
AI-First/
├── config/
│   └── config.py           # Configuration module
├── src/
│   ├── crawler.py          # Web crawling module
│   ├── text_cleaner.py     # Text cleaning and chunking
│   ├── embeddings.py       # Embedding generation
│   ├── vector_db.py        # Vector database operations
│   ├── qa_engine.py        # Q&A engine with RAG
│   ├── api.py              # Flask API server
│   └── __init__.py
├── data/
│   └── (crawled data will be stored here)
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
└── README.md              # This file
```

## Usage

### 1. Running the API Server

Start the Flask API:
```bash
cd src
python api.py
```

The server will start on `http://localhost:5000`

### 2. API Endpoints

#### Health Check
```bash
GET http://localhost:5000/health
```

#### Crawl Website
Before answering questions, you need to crawl and index a website:

```bash
curl -X POST http://localhost:5000/api/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "max_pages": 50,
    "crawl_delay": 1
  }'
```

**Parameters:**
- `url` (required) - Website URL to crawl
- `max_pages` (optional) - Maximum pages to crawl (default: 50)
- `crawl_delay` (optional) - Delay between requests in seconds (default: 1)

**Response:**
```json
{
  "status": "success",
  "pages_crawled": 10,
  "chunks_created": 45,
  "vector_db_stats": {...}
}
```

#### Ask a Question
After crawling, ask questions based on the crawled content:

```bash
curl -X POST http://localhost:5000/api/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is your product?",
    "top_k": 5,
    "temperature": 0.7
  }'
```

**Parameters:**
- `question` (required) - Your question
- `top_k` (optional) - Number of context chunks to retrieve (1-10, default: 5)
- `temperature` (optional) - LLM temperature for generation (0-2, default: 0.7)

**Response:**
```json
{
  "query": "What is your product?",
  "answer": "Based on the documentation...",
  "sources": [
    {
      "url": "https://example.com/about",
      "title": "About Us",
      "score": 0.92
    }
  ]
}
```

#### Get Database Statistics
```bash
curl http://localhost:5000/api/stats
```

#### Clear Database
```bash
curl -X POST http://localhost:5000/api/clear
```

## Complete Workflow Example

### 1. Prepare Environment
```bash
# Set up virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start API Server
```bash
cd src
python api.py
```

### 3. Crawl a Website
```bash
curl -X POST http://localhost:5000/api/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://python.org",
    "max_pages": 20,
    "crawl_delay": 2
  }'
```

### 4. Ask Questions
```bash
# Question 1
curl -X POST http://localhost:5000/api/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?"
  }'

# Question 2
curl -X POST http://localhost:5000/api/question \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I get started with Python?",
    "top_k": 3
  }'
```

## Testing with Postman

1. **Import the API:**
   - Create a new collection in Postman
   - Add requests for each endpoint

2. **Test Health:**
   - Method: GET
   - URL: `http://localhost:5000/health`

3. **Test Crawl:**
   - Method: POST
   - URL: `http://localhost:5000/api/crawl`
   - Body (raw JSON):
   ```json
   {
     "url": "https://example.com",
     "max_pages": 20
   }
   ```

4. **Test Question:**
   - Method: POST
   - URL: `http://localhost:5000/api/question`
   - Body (raw JSON):
   ```json
   {
     "question": "Your question here?"
   }
   ```

## Key Features

### Web Crawler
- Respects robots.txt and site boundaries
- Automatic URL deduplication
- Configurable crawl delay for politeness
- HTML parsing and content extraction
- Excludes non-content pages (login, logout, PDFs, etc.)

### Text Processing
- Removes HTML and special characters
- Automatic text chunking with overlap
- Sentence-aware splitting for better context
- Configurable chunk size

### Embeddings
- Uses OpenAI's `text-embedding-3-small` model
- Batch processing for efficiency
- 1536-dimensional embeddings

### Vector Database
- Pinecone for scalable vector storage
- Metadata preservation for source tracking
- Fast similarity search
- Batch upsert operations

### Q&A Engine
- Retrieval Augmented Generation (RAG) approach
- Context-aware answer generation
- Source attribution
- Temperature control for response variation

## Configuration

### Chunk Size
- Default: 500 characters
- Increase for longer context windows
- Decrease for more specific answers

### Temperature
- 0: Deterministic answers
- 0.7: Balanced (default)
- 2: Creative answers

### Top-K
- Number of context chunks to retrieve
- Higher = more context but slower
- Default: 5

## Troubleshooting

### Error: "API key not found"
- Ensure `.env` file exists and contains your API keys
- Check that environment variables are loaded correctly

### Error: "Index not found"
- Create a Pinecone index with the name specified in `.env`
- Check Pinecone API key and environment

### Slow Response Times
- Reduce `max_pages` in crawl request
- Reduce `top_k` in question request
- Check network connectivity

### Poor Answer Quality
- Ensure website was crawled with sufficient pages
- Check if question is related to crawled content
- Try with different `temperature` values

## Advanced Usage

### Custom Chunking Strategy
Edit `config/config.py`:
```python
CHUNK_SIZE = 1000  # Larger chunks
CHUNK_OVERLAP = 100  # More overlap
```

### Custom Embedding Model
In `.env`:
```
EMBEDDING_MODEL=text-embedding-3-large
```

### Custom LLM Model
In `.env`:
```
LLM_MODEL=gpt-4
```

## Performance Considerations

- **Memory**: Vector embeddings consume ~6KB per document
- **Cost**: OpenAI API charges per token (~$0.02 per 1M tokens for embeddings)
- **Speed**: Batch embedding generation is faster than individual requests
- **Database**: Pinecone has free tier with 2GB storage

## Limitations

- Crawls only text content (no PDFs, images, or videos)
- Respects HTTP redirects but may miss some content
- Requires active internet connection for crawling
- API rate limits apply from OpenAI and Pinecone

## Future Enhancements

- [ ] Support for multiple websites
- [ ] Web UI for easier interaction
- [ ] PDF and document support
- [ ] Multi-language support
- [ ] Real-time crawl updates
- [ ] Analytics and usage tracking
- [ ] Caching for repeated questions
- [ ] Fine-tuning on domain-specific data

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please check:
1. Environment variables are correctly set
2. API keys have necessary permissions
3. Internet connection is stable
4. API rate limits haven't been exceeded

---

**Built with:** Python, OpenAI, Pinecone, Flask  
**Version:** 1.0.0  
**Last Updated:** 2026-01-31