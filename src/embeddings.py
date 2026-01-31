"""
Embeddings Module
Generates embeddings for text chunks
"""
import logging
from typing import List, Dict
import numpy as np

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingsGenerator:
    """
    Generates embeddings for text using OpenAI API
    """
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """
        Initialize embeddings generator
        
        Args:
            api_key: OpenAI API key
            model: Embedding model to use
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to generate embeddings for
            batch_size: Number of texts to process in one batch
            
        Returns:
            List of embeddings
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")
            
            try:
                response = self.client.embeddings.create(
                    input=batch,
                    model=self.model
                )
                
                # Sort by index to maintain order
                batch_embeddings = sorted(response.data, key=lambda x: x.index)
                embeddings.extend([item.embedding for item in batch_embeddings])
                
            except Exception as e:
                logger.error(f"Error in batch processing: {e}")
                raise
        
        return embeddings
    
    def embed_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Add embeddings to documents
        
        Args:
            documents: List of documents to embed
            
        Returns:
            Documents with added embedding field
        """
        contents = [doc['content'] for doc in documents]
        embeddings = self.generate_embeddings_batch(contents)
        
        for doc, embedding in zip(documents, embeddings):
            doc['embedding'] = embedding
        
        logger.info(f"Generated embeddings for {len(documents)} documents")
        return documents


def generate_embeddings(api_key: str, documents: List[Dict], model: str = "text-embedding-3-small") -> List[Dict]:
    """
    Convenience function to generate embeddings
    """
    generator = EmbeddingsGenerator(api_key, model)
    return generator.embed_documents(documents)
