#!/bin/bash
# Quick test script for RAG Q&A Bot API

API_URL="http://localhost:5000"

echo "=========================================="
echo "RAG Q&A Bot - API Test Script"
echo "=========================================="

# Test 1: Health check
echo -e "\n1. Testing Health Check..."
curl -s "$API_URL/health" | jq .

# Test 2: Crawl website (example)
echo -e "\n2. Crawling website..."
curl -s -X POST "$API_URL/api/crawl" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "max_pages": 5,
    "crawl_delay": 2
  }' | jq .

# Test 3: Get stats
echo -e "\n3. Getting database statistics..."
curl -s "$API_URL/api/stats" | jq .

# Test 4: Ask a question
echo -e "\n4. Asking a question..."
curl -s -X POST "$API_URL/api/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic of this website?",
    "top_k": 3
  }' | jq .

echo -e "\n=========================================="
echo "Tests completed!"
echo "=========================================="
