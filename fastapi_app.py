from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
import requests
import numpy as np
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Load the blocks with vectors
with open("qa_blocks_with_vectors.json", "r", encoding="utf-8") as f:
    qa_blocks = json.load(f)

# Load the same embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FastAPI app
app = FastAPI()

# Pydantic models
class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    feedback: str

# Helper functions
def get_top_k_similar_blocks(query, qa_blocks, model, k=3):
    query_vec = model.encode([query])[0]
    similarities = []
    for block in qa_blocks:
        block_vec = np.array(block["vector"])
        sim = np.dot(query_vec, block_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(block_vec))
        similarities.append(sim)
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    return [qa_blocks[i] for i in top_k_indices]

def get_deepseek_answer(query, top_blocks):
    context = "\n\n".join([
        f"Block {i+1}:\nQuestion: {block['question']}\nAnswer: {block['answer']}" for i, block in enumerate(top_blocks)
    ])
    prompt = (
        f"Given the following blocks from a knowledge base, answer the user's question as best as possible. "
        f"If the answer is not present, say so.\n\n"
        f"User's question: {query}\n\n"
        f"Blocks:\n{context}\n\n"
        f"Summarize and answer the question using the most relevant information. "
        f"Also, specify which block(s) the answer was taken from. If any block has links, show them; otherwise, say 'No links'."
    )
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes and answers based on provided blocks."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        cleaned_answer = answer.replace('*', '').strip()
        return cleaned_answer
    else:
        raise HTTPException(status_code=500, detail="Error from OpenRouter API: " + response.text)

def save_feedback(question, answer, feedback):
    feedback_entry = {
        "question": question,
        "answer": answer,
        "feedback": feedback
    }
    feedback_file = "feedback.jsonl"
    with open(feedback_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(feedback_entry) + "\n")

# Endpoints
@app.post("/query")
def query_endpoint(request: QueryRequest):
    top_blocks = get_top_k_similar_blocks(request.query, qa_blocks, model, k=3)
    answer = get_deepseek_answer(request.query, top_blocks)
    return {"answer": answer}

@app.post("/feedback")
def feedback_endpoint(request: FeedbackRequest):
    save_feedback(request.question, request.answer, request.feedback)
    return {"status": "success", "message": "Feedback saved."} 