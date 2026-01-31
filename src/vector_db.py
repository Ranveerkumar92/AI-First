"""
Vector Database Module
Manages storage and retrieval of embeddings using ChromaDB
"""
import logging
import chromadb
from chromadb.config import Settings
from typing import List, Dict

logger = logging.getLogger(__name__)


class VectorDatabase:
    def __init__(self, db_path: str = "./data/chroma_db"):
        """
        Initialize ChromaDB vector database
        
        Args:
            db_path: Path to store the database
        """
        logger.info(f"Initializing ChromaDB at: {db_path}")
        
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=db_path,
            anonymized_telemetry=False,
        )
        
        self.client = chromadb.Client(settings)
        self.collection = None
        
    def create_collection(self, collection_name: str = "rag_documents"):
        """Create or get a collection"""
        logger.info(f"Creating collection: {collection_name}")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection created successfully")
    
    def add_documents(self, documents: List[Dict], embeddings: List[List[float]]):
        """
        Add documents and embeddings to the collection
        
        Args:
            documents: List of dicts with 'id', 'content', 'source' keys
            embeddings: List of embedding vectors
        """
        if not self.collection:
            self.create_collection()
        
        ids = [doc['id'] for doc in documents]
        metadatas = [{'source': doc.get('source', 'unknown')} for doc in documents]
        documents_text = [doc['content'] for doc in documents]
        
        logger.info(f"Adding {len(documents)} documents to collection")
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents_text,
            metadatas=metadatas
        )
        logger.info("Documents added successfully")
    
    def search(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        """
        Search for similar documents
        
        Args:
            query_embedding: Embedding vector of the query
            n_results: Number of results to return
            
        Returns:
            Search results with documents and distances
        """
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
    
    def persist(self):
        """Persist the database to disk"""
        logger.info("Persisting database")
        self.client.persist()
