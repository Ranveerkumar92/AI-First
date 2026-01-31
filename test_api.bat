@echo off
REM Quick test script for RAG Q&A Bot API (Windows)

setlocal enabledelayedexpansion

set API_URL=http://localhost:5000

echo.
echo ==========================================
echo RAG Q&A Bot - API Test Script
echo ==========================================

REM Test 1: Health check
echo.
echo 1. Testing Health Check...
curl -s "%API_URL%/health"

REM Test 2: Get stats
echo.
echo.
echo 2. Getting database statistics...
curl -s "%API_URL%/api/stats"

REM Test 3: Ask a question
echo.
echo.
echo 3. Asking a question...
curl -X POST "%API_URL%/api/question" ^
  -H "Content-Type: application/json" ^
  -d "{"question": "What is covered in this website?", "top_k": 3}"

echo.
echo ==========================================
echo Tests completed!
echo ==========================================
