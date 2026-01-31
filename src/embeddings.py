"""
Embeddings Module
Generates embeddings for text chunks using sentence-transformers
"""
import logging
from typing import List
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class EmbeddingsGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embeddings generator
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        logger.info(f"Loading embeddings model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Embeddings model loaded successfully")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Single text string
            
        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text)
        return embedding.tolist()
