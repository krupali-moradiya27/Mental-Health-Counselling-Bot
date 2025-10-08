import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# File paths
base_dir = os.path.dirname(__file__)
index_path = os.path.join(base_dir, "mental_health_index.faiss")
metadata_path = os.path.join(base_dir, "chunk_metadata.json")
urdu_data_path = os.path.join(base_dir, "urdu_data")

# Load existing FAISS index and metadata
index = faiss.read_index(index_path)

with open(metadata_path, "r", encoding="utf-8") as f:
    chunk_metadata = json.load(f)

# Track the current length for indexing
doc_index_offset = len(chunk_metadata)

# Load Urdu JSON files
all_data = []
for file in os.listdir(urdu_data_path):
    if file.endswith(".json"):
        with open(os.path.join(urdu_data_path, file), "r", encoding="utf-8") as f:
            all_data.extend(json.load(f))

# Process new Urdu data
new_embeddings = []
new_metadata = []

for i, item in enumerate(all_data):
    question = item.get("question", "")
    answer = item.get("answer", "")
    text = f"{question} {answer}".strip()

    if text:
        embedding = model.encode(text)
        new_embeddings.append(embedding)
        new_metadata.append({
            "doc_index": doc_index_offset + i,
            "text": text
        })

# Convert to numpy array
if new_embeddings:
    new_embeddings = np.array(new_embeddings).astype("float32")
    index.add(new_embeddings)  # Append to existing index

    # Update FAISS and metadata
    faiss.write_index(index, index_path)

    chunk_metadata.extend(new_metadata)
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(chunk_metadata, f, ensure_ascii=False, indent=2)

    print("✅ Urdu data appended to FAISS index successfully.")
else:
    print("⚠️ No Urdu data found to process.")
