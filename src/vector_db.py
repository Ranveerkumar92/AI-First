"""
Vector Database Module
Manages storing and retrieving embeddings from Pinecone
"""
import logging
from typing import List, Dict, Tuple
import time

try:
    from pinecone import Pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDatabase:
    """
    Manages vector embeddings in Pinecone
    """
    
    def __init__(self, api_key: str, environment: str, index_name: str):
        """
        Initialize vector database connection
        
        Args:
            api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Name of the index
        """
        if not PINECONE_AVAILABLE:
            raise ImportError("Pinecone package not installed")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        self.index = self.pc.Index(index_name)
        logger.info(f"Connected to Pinecone index: {index_name}")
    
    def upsert_vectors(self, documents: List[Dict], batch_size: int = 100):
        """
        Upload documents with embeddings to Pinecone
        
        Args:
            documents: List of documents with embeddings
            batch_size: Number of documents to upsert at once
        """
        vectors_to_upsert = []
        
        for i, doc in enumerate(documents):
            # Create unique ID
            doc_id = f"{doc['url']}#{doc['chunk_index']}"
            
            # Prepare metadata (without embedding)
            metadata = {
                'url': doc['url'],
                'title': doc['title'],
                'content': doc['content'],
                'chunk_index': doc['chunk_index']
            }
            
            # Create vector tuple (id, embedding, metadata)
            vector = (doc_id, doc['embedding'], metadata)
            vectors_to_upsert.append(vector)
            
            # Upsert in batches
            if len(vectors_to_upsert) >= batch_size or i == len(documents) - 1:
                try:
                    self.index.upsert(vectors=vectors_to_upsert)
                    logger.info(f"Upserted {len(vectors_to_upsert)} vectors")
                    vectors_to_upsert = []
                    time.sleep(1)  # Rate limiting
                except Exception as e:
                    logger.error(f"Error upserting vectors: {e}")
                    raise
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Embedding vector of the query
            top_k: Number of top results to return
            
        Returns:
            List of matching documents
        """
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            documents = []
            for match in results['matches']:
                doc = match['metadata']
                doc['score'] = match['score']
                documents.append(doc)
            
            return documents
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise
    
    def delete_all(self):
        """
        Delete all vectors from the index
        """
        try:
            self.index.delete(delete_all=True)
            logger.info("All vectors deleted from index")
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            raise
    
    def get_index_stats(self) -> Dict:
        """
        Get statistics about the index
        
        Returns:
            Index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            raise


def setup_vector_db(api_key: str, environment: str, index_name: str) -> VectorDatabase:
    """
    Convenience function to setup vector database
    """
    return VectorDatabase(api_key, environment, index_name)
