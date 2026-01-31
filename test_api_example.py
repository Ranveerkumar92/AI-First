"""
Example Python script to test the RAG Q&A Bot API
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5000"

def health_check():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def crawl_website(url, max_pages=20, crawl_delay=2):
    """Crawl a website"""
    print(f"Crawling website: {url}")
    
    payload = {
        "url": url,
        "max_pages": max_pages,
        "crawl_delay": crawl_delay
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/crawl",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}\n")
    return result


def ask_question(question, top_k=5, temperature=0.7):
    """Ask a question"""
    print(f"Question: {question}")
    
    payload = {
        "question": question,
        "top_k": top_k,
        "temperature": temperature
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/question",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    print(f"Answer: {result.get('answer', 'No answer')}")
    print(f"Sources:")
    for source in result.get('sources', []):
        print(f"  - {source['title']} ({source['url']}) - Score: {source['score']:.2f}")
    print()
    
    return result


def get_stats():
    """Get database statistics"""
    print("Getting database statistics...")
    response = requests.get(f"{API_BASE_URL}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def clear_database():
    """Clear the database"""
    print("Clearing database...")
    response = requests.post(f"{API_BASE_URL}/api/clear")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def main():
    """Run tests"""
    print("=" * 50)
    print("RAG Q&A Bot - API Testing")
    print("=" * 50 + "\n")
    
    try:
        # Test health
        health_check()
        time.sleep(1)
        
        # Test crawling (replace with actual website)
        print("CRAWLING PHASE")
        print("-" * 50)
        crawl_website("https://example.com", max_pages=5, crawl_delay=2)
        time.sleep(2)
        
        # Get stats
        get_stats()
        time.sleep(1)
        
        # Test questions
        print("QUESTION & ANSWER PHASE")
        print("-" * 50)
        ask_question("What is the main topic?", top_k=3)
        time.sleep(1)
        
        ask_question("Who created this website?", top_k=5)
        time.sleep(1)
        
        ask_question("How can I learn more?", top_k=3, temperature=0.5)
        
        print("=" * 50)
        print("All tests completed!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API server.")
        print("Make sure the API is running: python src/api.py")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
