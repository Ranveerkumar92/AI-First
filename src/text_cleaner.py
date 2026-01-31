"""
Text Cleaner Module
Cleans and chunks text for embeddings
"""
import re
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Cleans and processes text
    """
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize text cleaner
        
        Args:
            chunk_size: Size of text chunks
            overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and special characters
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.!?,;:\'-]', '', text)
        
        # Remove multiple punctuation
        text = re.sub(r'[.!?,;:]{2,}', '.', text)
        
        return text.strip()
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of chunks (uses default if not provided)
            overlap: Overlap size (uses default if not provided)
            
        Returns:
            List of text chunks
        """
        if chunk_size is None:
            chunk_size = self.chunk_size
        if overlap is None:
            overlap = self.overlap
            
        # Split by sentences first
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Add sentence to current chunk
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if len(test_chunk) <= chunk_size:
                current_chunk = test_chunk
            else:
                # Save current chunk if not empty
                if current_chunk:
                    chunks.append(current_chunk)
                
                # Start new chunk with overlap
                if chunks:
                    # Keep last 'overlap' characters from previous chunk
                    overlap_text = chunks[-1][-overlap:] if len(chunks[-1]) >= overlap else chunks[-1]
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
        
        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def process_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Process crawled documents by cleaning and chunking
        
        Args:
            documents: List of crawled documents
            
        Returns:
            List of processed documents with chunks
        """
        processed_docs = []
        
        for doc in documents:
            # Clean the content
            cleaned_content = self.clean_text(doc['content'])
            
            # Skip if content is too short
            if len(cleaned_content) < 50:
                continue
            
            # Chunk the content
            chunks = self.chunk_text(cleaned_content)
            
            # Create document entries for each chunk
            for i, chunk in enumerate(chunks):
                processed_docs.append({
                    'url': doc['url'],
                    'title': doc['title'],
                    'content': chunk,
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                })
        
        logger.info(f"Processed {len(processed_docs)} chunks from {len(documents)} documents")
        return processed_docs


def clean_and_chunk(documents: List[Dict], chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """
    Convenience function to clean and chunk documents
    """
    cleaner = TextCleaner(chunk_size, overlap)
    return cleaner.process_documents(documents)
