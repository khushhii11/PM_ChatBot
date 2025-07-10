import json
from sentence_transformers import SentenceTransformer

# Load Q&A content
with open("extracted_qa_content.json", "r", encoding="utf-8") as f:
    qa_blocks = json.load(f)

# Initialize the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Choose what to embed: concatenate question and answer
texts_to_embed = [block["question"] + " " + block["answer"] for block in qa_blocks]

# Create embeddings
embeddings = model.encode(texts_to_embed, show_progress_bar=True)

# Add embedding as 'vector' metadata to each block
for block, emb in zip(qa_blocks, embeddings):
    block["vector"] = emb.tolist()

# Save updated blocks with vector metadata
with open("qa_blocks_with_vectors.json", "w", encoding="utf-8") as f:
    json.dump(qa_blocks, f, indent=2)

print(f"Added vector embeddings to {len(qa_blocks)} Q&A blocks. Saved to qa_blocks_with_vectors.json.") 