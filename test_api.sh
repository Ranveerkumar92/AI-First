#!/bin/bash
# Test script for RAG Q&A API

echo "Starting RAG Q&A Bot API Tests..."
echo ""

# Base URL
BASE_URL="http://localhost:5000"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Test 1: Health Check${NC}"
curl -X GET "$BASE_URL/health"
echo -e "\n\n"

echo -e "${BLUE}Test 2: Get Statistics${NC}"
curl -X GET "$BASE_URL/api/stats"
echo -e "\n\n"

echo -e "${BLUE}Test 3: Ask a Question${NC}"
curl -X POST "$BASE_URL/api/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this website about?",
    "top_k": 3
  }'
echo -e "\n\n"

echo -e "${BLUE}Test 4: Ask Another Question${NC}"
curl -X POST "$BASE_URL/api/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Tell me about the key features",
    "top_k": 5
  }'
echo -e "\n\n"

echo -e "${GREEN}Tests completed!${NC}"
