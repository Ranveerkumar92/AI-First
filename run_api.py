#!/usr/bin/env python
"""
Main entry point for running the Flask API server
Usage: python run_api.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main function"""
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("\n" + "=" * 70)
    print("RAG Q&A SUPPORT BOT - API SERVER")
    print("=" * 70)
    print(f"\nConfiguration:")
    print(f"  Port: {port}")
    print(f"  Debug Mode: {debug}")
    print(f"  Database Path: {os.getenv('VECTOR_DB_PATH', './data/chroma_db')}")
    print(f"\nStarting API server...")
    print("=" * 70)
    print(f"\n✓ API Server running at http://0.0.0.0:{port}")
    print(f"\nAvailable endpoints:")
    print(f"  GET  http://localhost:{port}/health")
    print(f"  GET  http://localhost:{port}/api/stats")
    print(f"  POST http://localhost:{port}/api/ask")
    print(f"\nPress CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    try:
        # Import and run the Flask app
        from src.api import app, initialize_components
        
        # Initialize components before starting server
        initialize_components()
        
        # Run the server
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False
        )
        
    except ImportError as e:
        print(f"ERROR: Failed to import Flask app. Please ensure dependencies are installed.")
        print(f"Details: {str(e)}")
        print("\nTo fix, run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to start API server")
        print(f"Details: {str(e)}")
        print("\nPlease check:")
        print("1. Port is not in use")
        print("2. Vector database exists (run 'python index_data.py' first)")
        print("3. All dependencies are installed")
        sys.exit(1)

if __name__ == "__main__":
    main()
