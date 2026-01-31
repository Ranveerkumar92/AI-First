# Postman Collection for RAG Q&A Support Bot

This collection contains all API endpoints for the RAG Q&A Support Bot.

## Endpoints

### 1. Health Check
- **URL**: `http://localhost:5000/health`
- **Method**: GET
- **Description**: Check if the API is running
- **Response**: Status indicator

### 2. Statistics
- **URL**: `http://localhost:5000/api/stats`
- **Method**: GET
- **Description**: Get collection statistics
- **Response**: Collection name and total documents

### 3. Ask Question
- **URL**: `http://localhost:5000/api/ask`
- **Method**: POST
- **Headers**: 
  - `Content-Type: application/json`
- **Body**:
```json
{
  "question": "What is this website about?",
  "top_k": 5
}
```
- **Response**: Retrieved documents with rankings and distances

## Import to Postman

1. Open Postman
2. Click "Import"
3. Copy-paste this collection or upload from file
4. Set the base URL: `{{base_url}}`
5. Create environment variable: `base_url=http://localhost:5000`

## Testing Workflow

1. Start API server: `python run_api.py`
2. Test Health Check first
3. Test Stats endpoint
4. Test Ask Question with different queries

## Sample Questions to Try

- "What services are offered?"
- "Tell me about the main features"
- "What is the company's history?"
- "How can I contact support?"
- "What are the pricing options?"

## Response Format

All endpoints return JSON in the following format:

**Success Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "status": "error"
}
```
