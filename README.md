# RAG Q&A Support Bot

A Retrieval Augmented Generation (RAG) based question-answering system that crawls websites, indexes content, and provides intelligent Q&A through a REST API.

## Overview

This project implements a complete RAG workflow:

1. **Web Crawling**: Automatically crawls and extracts content from target websites
2. **Text Processing**: Cleans and chunks content into manageable pieces
3. **Embeddings**: Generates semantic embeddings using sentence transformers
4. **Vector Storage**: Stores embeddings in ChromaDB for fast retrieval
5. **Q&A API**: Flask-based REST API for answering questions from indexed content

## Features

- ✅ Automatic website crawling with domain filtering
- ✅ Intelligent text cleaning and preprocessing
- ✅ Semantic embedding generation
- ✅ Fast vector-based retrieval
- ✅ RESTful API endpoints
- ✅ Comprehensive logging and error handling
- ✅ Easy configuration via environment variables

## Prerequisites

- Python 3.8+
- pip package manager
- Git
- curl or Postman (for API testing)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-First
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your configuration:
   # - OPENAI_API_KEY (if using OpenAI)
   # - TARGET_WEBSITE (URL to crawl)
   # - VECTOR_DB_PATH (path to store database)
   # - FLASK_PORT (API port, default 5000)
   ```

## Configuration

Edit `.env` file to configure:

```env
# OpenAI API Configuration (optional for future enhancement)
OPENAI_API_KEY=your_openai_api_key_here

# Website to Crawl
TARGET_WEBSITE=https://example.com

# Vector Database Configuration
VECTOR_DB_PATH=./data/chroma_db

# API Configuration
FLASK_ENV=development
FLASK_PORT=5000
```

## Project Structure

```
AI-First/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── crawler.py           # Web crawler module
│   ├── cleaner.py           # Text cleaning module
│   ├── embeddings.py        # Embeddings generation
│   ├── vector_db.py         # Vector database management
│   ├── pipeline.py          # Complete indexing pipeline
│   └── api.py               # Flask API
├── data/                    # Data storage (gitignored)
├── config/                  # Configuration files
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment file
├── .gitignore              # Git ignore file
├── test_api.sh            # API test script (Linux/macOS)
├── test_api.bat           # API test script (Windows)
├── index_data.py          # Main script to index website
├── run_api.py             # Main script to start API server
└── README.md              # This file
```

## Usage

### Step 1: Prepare Environment

```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Update .env with your website URL
```

### Step 2: Index Website Content

```bash
# Run the indexing pipeline
python index_data.py

# This will:
# 1. Crawl the website (up to max_pages)
# 2. Clean and chunk the content
# 3. Generate embeddings
# 4. Store in vector database
```

Expected output:
```
==================================================
Starting RAG Indexing Pipeline
==================================================

[Step 1/4] Crawling website...
Crawled 25 pages

[Step 2/4] Cleaning and chunking content...
Created 150 document chunks

[Step 3/4] Generating embeddings...
Generated 150 embeddings

[Step 4/4] Storing in vector database...

==================================================
Indexing Pipeline Completed Successfully!
==================================================
```

### Step 3: Start API Server

```bash
# Run the Flask API server
python run_api.py

# Server will start at http://localhost:5000
```

Output:
```
 * Running on http://0.0.0.0:5000
```

### Step 4: Query the API

**Health Check:**
```bash
curl -X GET http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "RAG Q&A Support Bot"
}
```

**Get Statistics:**
```bash
curl -X GET http://localhost:5000/api/stats
```

Response:
```json
{
  "status": "success",
  "stats": {
    "collection_name": "rag_documents",
    "total_documents": 150
  }
}
```

**Ask a Question:**
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What services do you offer?",
    "top_k": 5
  }'
```

Response:
```json
{
  "question": "What services do you offer?",
  "retrieved_documents": [
    {
      "rank": 1,
      "content": "We offer comprehensive web development services including...",
      "source": "https://example.com/services",
      "distance": 0.125
    },
    ...
  ],
  "total_results": 5,
  "status": "success"
}
```

## API Endpoints

### 1. Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the API is running
- **Response**: Status message

### 2. Statistics
- **Endpoint**: `GET /api/stats`
- **Description**: Get statistics about indexed content
- **Response**: Collection name and total document count

### 3. Ask Question
- **Endpoint**: `POST /api/ask`
- **Description**: Submit a question and retrieve relevant documents
- **Request Body**:
  ```json
  {
    "question": "Your question here",
    "top_k": 5
  }
  ```
- **Response**: Question, retrieved documents, and metadata

## Testing

### Using the Test Scripts

**Windows:**
```bash
test_api.bat
```

**Linux/macOS:**
```bash
bash test_api.sh
```

### Using Postman

1. Import the API endpoints
2. Create requests for each endpoint
3. Test with various questions
4. Verify response structure

### Using curl

```bash
# Test 1: Health check
curl http://localhost:5000/health

# Test 2: Get stats
curl http://localhost:5000/api/stats

# Test 3: Ask question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question", "top_k": 5}'
```

## Architecture

### Workflow

```
Website URL
    ↓
[Web Crawler] → Extract HTML pages
    ↓
[Text Cleaner] → Clean & Chunk text
    ↓
[Embeddings Generator] → Generate vectors
    ↓
[Vector Database] → Store embeddings
    ↓
[Vector Database] ← Query embeddings
    ↓
[Retrieval Results] → Flask API
    ↓
User Question/Answer
```

### Components

1. **Crawler**: BeautifulSoup-based web crawler
   - Domain-restricted crawling
   - Automatic HTML to text extraction
   - Recursive link discovery

2. **Cleaner**: Text preprocessing
   - Whitespace normalization
   - URL and email removal
   - Overlapping chunk generation

3. **Embeddings**: Semantic vectorization
   - Uses `all-MiniLM-L6-v2` model by default
   - Batch processing support
   - Single text embedding capability

4. **Vector DB**: ChromaDB-based storage
   - Persistent storage
   - Cosine similarity search
   - Metadata tracking

5. **API**: Flask REST interface
   - Stateless design
   - Error handling
   - JSON request/response

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution**: Make sure you're running scripts from the project root directory

### Issue: "Connection refused" when accessing API
**Solution**: Ensure the Flask server is running and listening on the correct port

### Issue: No documents retrieved
**Solution**: 
- Verify website was crawled successfully (check logs)
- Check if vector database was created (look in `data/chroma_db`)
- Try different search queries

### Issue: Slow embeddings generation
**Solution**: This is normal for large datasets. Consider:
- Using a smaller model
- Reducing chunk size
- Processing in batches

### Issue: Out of memory during embeddings
**Solution**:
- Reduce chunk size
- Reduce max_pages
- Process in smaller batches

## Performance Tips

1. **Adjust chunk size**: Balance between semantic meaning and retrieval speed
   - Smaller chunks (100-300): More precise but more chunks
   - Larger chunks (500-1000): Less precise but fewer chunks

2. **Embedding model**: 
   - `all-MiniLM-L6-v2` (default): Fast, low memory
   - `all-mpnet-base-v2`: More accurate, higher memory

3. **Database optimization**:
   - Regular persist operations
   - Monitor collection size
   - Archive old data if needed

## Technologies Used

- **Python 3.8+**: Core language
- **Flask**: Web framework
- **BeautifulSoup4**: HTML parsing
- **SentenceTransformers**: Embeddings generation
- **ChromaDB**: Vector database
- **Requests**: HTTP client
- **python-dotenv**: Environment configuration

## Future Enhancements

- [ ] Integration with OpenAI for answer generation
- [ ] Support for multiple websites
- [ ] Advanced filtering and date-based queries
- [ ] Caching layer for frequent queries
- [ ] Web UI dashboard
- [ ] Authentication and rate limiting
- [ ] Database backup and recovery
- [ ] Multi-language support

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify configuration settings
4. Check internet connectivity for crawling

## Notes

- The system only answers questions based on crawled content
- Crawling respects domain boundaries (same domain only)
- Embeddings are cached in the vector database
- All content is stored locally in `data/` directory