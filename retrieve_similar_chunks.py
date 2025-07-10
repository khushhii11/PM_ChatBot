import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the blocks with vectors
with open("qa_blocks_with_vectors.json", "r", encoding="utf-8") as f:
    qa_blocks = json.load(f)

# Load the same embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_top_k_similar_blocks(query, qa_blocks, model, k=3):
    # Encode the query
    query_vec = model.encode([query])[0]
    # Compute cosine similarity
    similarities = []
    for block in qa_blocks:
        block_vec = np.array(block["vector"])
        sim = np.dot(query_vec, block_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(block_vec))
        similarities.append(sim)
    # Get indices of top k
    top_k_indices = np.argsort(similarities)[-k:][::-1]
    # Return the top k blocks
    return [qa_blocks[i] for i in top_k_indices]

if __name__ == "__main__":
    query = input("Enter your query: ")
    top_blocks = get_top_k_similar_blocks(query, qa_blocks, model, k=3)
    for i, block in enumerate(top_blocks, 1):
        print(f"\nRank {i}:")
        print(f"ID: {block.get('id', 'N/A')}")
        print(f"Question: {block.get('question', 'N/A')}")
        print(f"Answer: {block.get('answer', 'N/A')}")
        links = block.get('links', [])
        if links:
            print(f"Links: {links}") 