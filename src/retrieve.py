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

def search_chunks(query, index, chunks, top_k=3):
    """Converts the user question to a vector and finds the closest text chunks."""
    print(f"[*] Searching for context related to: '{query}'...")
    
    # We must use the EXACT SAME embedding model we used in ingest.py
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Convert query to vector
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype('float32')
    
    # Search FAISS. Returns distances (how close they are) and indices (the chunk ID numbers)
    distances, indices = index.search(query_vector, top_k)
    
    # Retrieve the actual English text for those top matches
    retrieved_text = []
    for i in indices[0]:
        if i != -1: # -1 means no match found
            retrieved_text.append(chunks[i])
            
    return retrieved_text


def ask_llm(query, context_chunks):
    """Combines the context and query, then asks the local Mistral model."""
    print("[*] Generating answer using local LLM...")
    
    # Combine all the chunks into one big string of context
    context_string = "\n\n".join(context_chunks)
    
    # This is the "System Prompt" - the rules of engagement for the AI
    system_instruction = """
    You are a helpful company assistant. You will be provided with context from internal documents.
    Answer the user's question using ONLY the provided context. 
    If the answer is not in the context, say "I cannot find the answer in the provided documents."
    Do not make things up.
    """
    
    # Combine everything into the final prompt
    final_prompt = f"Context:\n{context_string}\n\nQuestion:\n{query}"
    
    # Send it to Ollama
    response = ollama.chat(model='mistral', messages=[
        {'role': 'system', 'content': system_instruction},
        {'role': 'user', 'content': final_prompt}
    ])
    
    return response['message']['content']

