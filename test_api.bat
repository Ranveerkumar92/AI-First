@echo off
REM Test script for RAG Q&A API (Windows)

setlocal enabledelayedexpansion
echo Starting RAG Q^&A Bot API Tests...
echo.

REM Base URL
set BASE_URL=http://localhost:5000

echo Test 1: Health Check
curl -X GET "%BASE_URL%/health"
echo.
echo.

echo Test 2: Get Statistics
curl -X GET "%BASE_URL%/api/stats"
echo.
echo.

echo Test 3: Ask a Question
curl -X POST "%BASE_URL%/api/ask" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is this website about?\", \"top_k\": 3}"
echo.
echo.

echo Test 4: Ask Another Question
curl -X POST "%BASE_URL%/api/ask" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"Tell me about the key features\", \"top_k\": 5}"
echo.
echo.

echo Tests completed!
