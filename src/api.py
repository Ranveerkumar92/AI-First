"""
Flask API for Q&A Support Bot
Provides endpoints for querying the RAG system
"""
import os
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.embeddings import EmbeddingsGenerator
from src.vector_db import VectorDatabase

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize components
vector_db = None
embeddings_gen = None


def initialize_components():
    """Initialize RAG components"""
    global vector_db, embeddings_gen
    
    db_path = os.getenv('VECTOR_DB_PATH', './data/chroma_db')
    
    logger.info("Initializing RAG components...")
    embeddings_gen = EmbeddingsGenerator()
    vector_db = VectorDatabase(db_path)
    vector_db.create_collection()
    logger.info("Components initialized successfully")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'RAG Q&A Support Bot'
    }), 200


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """
    Ask a question to the Q&A bot
    
    Expected JSON:
    {
        "question": "Your question here",
        "top_k": 5  (optional, default is 5)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing "question" field in request'
            }), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({
                'error': 'Question cannot be empty'
            }), 400
        
        top_k = data.get('top_k', 5)
        
        logger.info(f"Processing question: {question}")
        
        # Generate embedding for the question
        question_embedding = embeddings_gen.generate_single_embedding(question)
        
        # Search in vector database
        results = vector_db.search(question_embedding, n_results=top_k)
        
        # Format response
        retrieved_docs = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                retrieved_docs.append({
                    'rank': i + 1,
                    'content': doc,
                    'source': results['metadatas'][0][i]['source'],
                    'distance': float(results['distances'][0][i]) if results['distances'] else None
                })
        
        response = {
            'question': question,
            'retrieved_documents': retrieved_docs,
            'total_results': len(retrieved_docs),
            'status': 'success'
        }
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about the indexed content"""
    try:
        collection_stats = {
            'collection_name': vector_db.collection.name if vector_db.collection else None,
            'total_documents': vector_db.collection.count() if vector_db.collection else 0
        }
        
        return jsonify({
            'status': 'success',
            'stats': collection_stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve statistics',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    initialize_components()
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
