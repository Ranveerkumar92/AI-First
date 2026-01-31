"""
Flask API for Q&A Bot
"""
import json
import logging
import os
from typing import Tuple, Dict
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import configuration
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.config import (
    OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME,
    FLASK_PORT, TEMPERATURE, MAX_TOKENS
)

# Import modules
from crawler import WebCrawler
from text_cleaner import TextCleaner
from embeddings import EmbeddingsGenerator
from vector_db import VectorDatabase
from qa_engine import QAEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for modules (lazy loaded)
qa_engine = None


def get_qa_engine():
    """
    Lazy load and return QA engine
    """
    global qa_engine
    if qa_engine is None:
        try:
            embedding_gen = EmbeddingsGenerator(OPENAI_API_KEY)
            vector_db = VectorDatabase(PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME)
            qa_engine = QAEngine(OPENAI_API_KEY, vector_db, embedding_gen)
        except Exception as e:
            logger.error(f"Error initializing QA engine: {e}")
            raise
    return qa_engine


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint
    """
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/question', methods=['POST'])
def ask_question():
    """
    Main Q&A endpoint
    
    Expected JSON body:
    {
        "question": "What is...",
        "top_k": 5,
        "temperature": 0.7
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Missing required field: question'}), 400
        
        question = data['question']
        top_k = data.get('top_k', 5)
        temperature = data.get('temperature', TEMPERATURE)
        
        # Validate inputs
        if not isinstance(question, str) or len(question.strip()) == 0:
            return jsonify({'error': 'Question must be a non-empty string'}), 400
        
        if not isinstance(top_k, int) or top_k < 1 or top_k > 10:
            return jsonify({'error': 'top_k must be between 1 and 10'}), 400
        
        if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 2:
            return jsonify({'error': 'temperature must be between 0 and 2'}), 400
        
        # Get QA engine
        engine = get_qa_engine()
        
        # Generate answer
        result = engine.answer_question(question, top_k=top_k, temperature=temperature)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in ask_question: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/crawl', methods=['POST'])
def crawl_website():
    """
    Endpoint to crawl a website and prepare it for Q&A
    
    Expected JSON body:
    {
        "url": "https://example.com",
        "max_pages": 50,
        "crawl_delay": 1
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'Missing required field: url'}), 400
        
        url = data['url']
        max_pages = data.get('max_pages', 50)
        crawl_delay = data.get('crawl_delay', 1)
        
        # Validate inputs
        if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        logger.info(f"Starting crawl of {url}")
        
        # Step 1: Crawl website
        crawler = WebCrawler(url, max_pages=max_pages, delay=crawl_delay)
        crawled_data = crawler.crawl()
        
        logger.info(f"Crawled {len(crawled_data)} pages")
        
        # Step 2: Clean and chunk
        cleaner = TextCleaner()
        processed_data = cleaner.process_documents(crawled_data)
        
        logger.info(f"Processed into {len(processed_data)} chunks")
        
        # Step 3: Generate embeddings
        embeddings_gen = EmbeddingsGenerator(OPENAI_API_KEY)
        embedded_data = embeddings_gen.embed_documents(processed_data)
        
        # Step 4: Store in vector DB
        vector_db = VectorDatabase(PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME)
        vector_db.upsert_vectors(embedded_data)
        
        stats = vector_db.get_index_stats()
        
        return jsonify({
            'status': 'success',
            'pages_crawled': len(crawled_data),
            'chunks_created': len(embedded_data),
            'vector_db_stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error in crawl_website: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get vector database statistics
    """
    try:
        vector_db = VectorDatabase(PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME)
        stats = vector_db.get_index_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_database():
    """
    Clear all vectors from the database
    WARNING: This will delete all stored embeddings
    """
    try:
        vector_db = VectorDatabase(PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME)
        vector_db.delete_all()
        return jsonify({'status': 'success', 'message': 'Database cleared'}), 200
    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info(f"Starting API server on port {FLASK_PORT}")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=True)
