"""
Quick start guide and integration example
"""

# QUICK START EXAMPLE

# 1. First, set up your environment:
# $ python -m venv venv
# $ source venv/bin/activate  # On Windows: venv\Scripts\activate
# $ pip install -r requirements.txt

# 2. Configure your API keys in .env file

# 3. Start the API server:
# $ cd src
# $ python api.py

# 4. In another terminal, you can now:

import requests
import json

BASE_URL = "http://localhost:5000"

# A. Check if API is running
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# B. Crawl a website
crawl_request = {
    "url": "https://example.com",
    "max_pages": 20,
    "crawl_delay": 1
}
response = requests.post(f"{BASE_URL}/api/crawl", json=crawl_request)
print(json.dumps(response.json(), indent=2))

# C. Ask a question
question_request = {
    "question": "What is your product?",
    "top_k": 5,
    "temperature": 0.7
}
response = requests.post(f"{BASE_URL}/api/question", json=question_request)
result = response.json()

print(f"\nQuestion: {result['query']}")
print(f"Answer: {result['answer']}")
print(f"\nSources:")
for source in result['sources']:
    print(f"  - {source['title']}: {source['url']}")

# D. Get database stats
response = requests.get(f"{BASE_URL}/api/stats")
print(json.dumps(response.json(), indent=2))

# CURL EXAMPLES (use in terminal)

# Health check:
# curl http://localhost:5000/health

# Crawl website:
# curl -X POST http://localhost:5000/api/crawl \
#   -H "Content-Type: application/json" \
#   -d '{"url": "https://example.com", "max_pages": 20}'

# Ask question:
# curl -X POST http://localhost:5000/api/question \
#   -H "Content-Type: application/json" \
#   -d '{"question": "What is your product?", "top_k": 5}'

# Get stats:
# curl http://localhost:5000/api/stats

# Clear database:
# curl -X POST http://localhost:5000/api/clear
