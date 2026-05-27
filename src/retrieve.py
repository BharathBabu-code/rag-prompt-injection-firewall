import os
import json
import faiss
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

def load_database(db_dir="embeddings"):
    """Loads the FAISS index map and the JSON text chunks."""
    index_path = os.path.join(db_dir, "vector_index.faiss")
    chunks_path = os.path.join(db_dir, "chunks.json")
    
    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        raise FileNotFoundError("Database files not found. Did you run ingest.py first?")
        
    print("[*] Loading FAISS database and text chunks...")
    index = faiss.read_index(index_path)
    
    with open(chunks_path, "r") as f:
        chunks = json.load(f)
        
    return index, chunks