"""
Data Indexing Pipeline
Orchestrates the complete workflow: crawl, clean, embed, and store
"""
import logging
import os
from datetime import datetime
import json
from src.crawler import WebCrawler
from src.cleaner import TextCleaner
from src.embeddings import EmbeddingsGenerator
from src.vector_db import VectorDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexingPipeline:
    def __init__(self, website_url: str, db_path: str = "./data/chroma_db", 
                 max_pages: int = 50):
        """
        Initialize the indexing pipeline
        
        Args:
            website_url: URL of the website to crawl
            db_path: Path for the vector database
            max_pages: Maximum pages to crawl
        """
        self.website_url = website_url
        self.db_path = db_path
        self.max_pages = max_pages
        
        # Initialize components
        self.crawler = WebCrawler(website_url, max_pages)
        self.cleaner = TextCleaner()
        self.embeddings_gen = EmbeddingsGenerator()
        self.vector_db = VectorDatabase(db_path)
        self.vector_db.create_collection()
        
    def run(self):
        """Run the complete indexing pipeline"""
        logger.info("=" * 50)
        logger.info("Starting RAG Indexing Pipeline")
        logger.info("=" * 50)
        
        # Step 1: Crawl
        logger.info("\n[Step 1/4] Crawling website...")
        pages = self.crawler.crawl()
        logger.info(f"Crawled {len(pages)} pages")
        
        if not pages:
            logger.error("No pages crawled. Exiting.")
            return False
        
        # Step 2: Clean and chunk
        logger.info("\n[Step 2/4] Cleaning and chunking content...")
        documents = []
        all_chunks = []
        
        for idx, page in enumerate(pages):
            chunks = self.cleaner.process_content(page['content'])
            
            for chunk_idx, chunk in enumerate(chunks):
                doc_id = f"doc_{idx}_{chunk_idx}"
                documents.append({
                    'id': doc_id,
                    'content': chunk,
                    'source': page['url']
                })
                all_chunks.append(chunk)
        
        logger.info(f"Created {len(documents)} document chunks")
        
        # Step 3: Generate embeddings
        logger.info("\n[Step 3/4] Generating embeddings...")
        embeddings = self.embeddings_gen.generate_embeddings(all_chunks)
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        # Step 4: Store in vector database
        logger.info("\n[Step 4/4] Storing in vector database...")
        self.vector_db.add_documents(documents, embeddings)
        self.vector_db.persist()
        
        logger.info("\n" + "=" * 50)
        logger.info("Indexing Pipeline Completed Successfully!")
        logger.info("=" * 50)
        
        # Save metadata
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'website_url': self.website_url,
            'total_pages_crawled': len(pages),
            'total_chunks': len(documents),
            'db_path': self.db_path
        }
        
        os.makedirs(self.db_path, exist_ok=True)
        with open(os.path.join(self.db_path, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    website_url = os.getenv('TARGET_WEBSITE', 'https://example.com')
    db_path = os.getenv('VECTOR_DB_PATH', './data/chroma_db')
    
    pipeline = IndexingPipeline(website_url, db_path, max_pages=50)
    pipeline.run()
