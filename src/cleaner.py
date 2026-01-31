"""
Text Cleaning Module
Cleans and preprocesses text content
"""
import re
import logging

logger = logging.getLogger(__name__)


class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric, spaces, and basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\:\;]', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        step = chunk_size - overlap
        
        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    @staticmethod
    def process_content(content: str, chunk_size: int = 500, 
                       overlap: int = 50) -> list:
        """
        Complete processing pipeline: clean and chunk text
        
        Args:
            content: Raw content
            chunk_size: Size of chunks
            overlap: Overlap between chunks
            
        Returns:
            List of processed chunks
        """
        cleaned = TextCleaner.clean_text(content)
        chunks = TextCleaner.chunk_text(cleaned, chunk_size, overlap)
        return chunks
