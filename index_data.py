#!/usr/bin/env python
"""
Main entry point for indexing website content
Usage: python index_data.py
"""
import os
import sys
from dotenv import load_dotenv
from src.pipeline import IndexingPipeline

# Load environment variables
load_dotenv()

def main():
    """Main function"""
    website_url = os.getenv('TARGET_WEBSITE')
    db_path = os.getenv('VECTOR_DB_PATH', './data/chroma_db')
    
    if not website_url:
        print("ERROR: TARGET_WEBSITE not set in .env file")
        print("Please set TARGET_WEBSITE in .env and try again")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("RAG Q&A SUPPORT BOT - DATA INDEXING")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Target Website: {website_url}")
    print(f"  Database Path: {db_path}")
    print(f"\nStarting indexing process...")
    print("=" * 70 + "\n")
    
    try:
        pipeline = IndexingPipeline(
            website_url=website_url,
            db_path=db_path,
            max_pages=50
        )
        success = pipeline.run()
        
        if success:
            print("\n" + "=" * 70)
            print("✓ Indexing completed successfully!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Update .env with correct settings if needed")
            print("2. Run 'python run_api.py' to start the API server")
            print("3. Use the API to ask questions about the crawled content")
            print("=" * 70 + "\n")
            sys.exit(0)
        else:
            print("\n" + "=" * 70)
            print("✗ Indexing failed. Please check the logs above.")
            print("=" * 70 + "\n")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nPlease check:")
        print("1. Internet connectivity")
        print("2. TARGET_WEBSITE is valid and accessible")
        print("3. Sufficient disk space for database")
        sys.exit(1)

if __name__ == "__main__":
    main()
