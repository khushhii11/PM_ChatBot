# PMAccelerator RAGPM

## Overview
This project provides a Retrieval-Augmented Generation (RAG) pipeline for answering questions based on a knowledge base extracted from a Word document. It uses embeddings for semantic search and integrates with the DeepSeek R1 model via OpenRouter for answer generation and summarization. A FastAPI backend exposes endpoints for frontend integration and feedback collection.

## Features
- Extract Q&A blocks from a Word document
- Generate and store vector embeddings for semantic search
- Retrieve top relevant blocks for a user query
- Summarize and answer queries using DeepSeek R1 (OpenRouter API)
- FastAPI backend with endpoints for querying and feedback
- Feedback is saved for further analysis
- Environment variables managed securely via `.env`

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install fastapi uvicorn python-dotenv requests sentence-transformers
```

### 2. Prepare Data
- Place your Word document (`PMData.docx`) in the project root.
- Run the extraction and embedding scripts:
  ```bash
  python extract_docx_to_json.py
  python create_embeddings.py
  ```

### 3. Set Up API Key
- Create a `.env` file in the project root:
  ```
  OPENROUTER_API_KEY=your_openrouter_key_here
  ```
- Ensure `.env` is in `.gitignore` (already set).

### 4. Run the FastAPI Server
```bash
uvicorn fastapi_app:app --reload
```
- The API will be available at `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### POST `/query`
- **Description:** Submit a user query and get an answer.
- **Request Body:**
  ```json
  {
    "query": "What is the start date of the internship?"
  }
  ```
- **Response:**
  ```json
  {
    "answer": "The earliest start date is next week, depending on the completion of the assessment. ..."
  }
  ```

### POST `/feedback`
- **Description:** Submit feedback for a given question and answer.
- **Request Body:**
  ```json
  {
    "question": "What is the start date of the internship?",
    "answer": "The earliest start date is next week, depending on the completion of the assessment. ...",
    "feedback": "yes" // or "no"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Feedback saved."
  }
  ```

## Frontend Integration
- The frontend can POST to `/query` to get answers and to `/feedback` to submit user feedback.
- See the interactive docs at `/docs` for testing and schema.

## Security
- **API keys** are stored in `.env` and never committed to version control.
- **Feedback** is saved in `feedback.jsonl` for later analysis.

## Example JavaScript Fetch
```js
// Query endpoint
fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'What is the start date of the internship?' })
})
  .then(res => res.json())
  .then(data => console.log(data.answer));

// Feedback endpoint
fetch('http://localhost:8000/feedback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: 'What is the start date of the internship?',
    answer: 'The earliest start date is next week, depending on the completion of the assessment. ...',
    feedback: 'yes'
  })
});
```

## License
MIT 