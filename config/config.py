"""
Configuration module for RAG Q&A Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-qa-bot")

# Flask Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "development")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# Crawler Configuration
TARGET_URL = os.getenv("TARGET_URL", "https://example.com")
MAX_PAGES = int(os.getenv("MAX_PAGES", 50))
CRAWL_DELAY = float(os.getenv("CRAWL_DELAY", 1))

# Text Processing
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

# Embedding Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

# LLM Configuration
LLM_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 500

# File Paths
DATA_DIR = "data"
CRAWLED_DATA_FILE = os.path.join(DATA_DIR, "crawled_data.json")
PROCESSED_DATA_FILE = os.path.join(DATA_DIR, "processed_data.json")
