import os
import json
import faiss
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer
from detector import scan_and_redact

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

def search_and_sanitize_chunks(query, index, chunks, top_k=3):
    """Finds the closest text chunks AND runs them through the firewall."""
    print(f"[*] Searching for context related to: '{query}'...")
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype('float32')
    
    distances, indices = index.search(query_vector, top_k)
    
    safe_retrieved_text = []
    for i in indices[0]:
        if i != -1: 
            raw_chunk = chunks[i]
            
            # Pass the raw data through security detector
            safe_chunk, was_attack = scan_and_redact(raw_chunk)
            
            if was_attack:
                print(f"[!] Warning: Malicious payload intercepted in chunk {i}. Redacting.")
                
            safe_retrieved_text.append(safe_chunk)
            
    return safe_retrieved_text


def ask_llm(query, context_chunks):
    """Combines the context and query, then asks the local Mistral model."""
    print("[*] Generating answer using local LLM...")
    
    # Combine all the chunks into one big string of context
    context_string = "\n\n".join(context_chunks)
    
    # This is the "System Prompt" - the rules of engagement for the AI
    system_instruction = """
    You are a helpful company assistant. You will be provided with context from internal documents.
    Answer the user's question using ONLY the provided context. 
    If the context contains a [REDACTED] warning, inform the user that the source document was compromised.
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

if __name__ == "__main__":
    try:
        # 1. Load the database
        faiss_index, text_chunks = load_database()
        
        # 2. Define the question you want to ask about your PDF
        user_question = "What is the main topic of this document?"
        
        # 3. Find the most relevant chunks and checks if its safe
        relevant_chunks = search_and_sanitize_chunks(user_question, faiss_index, text_chunks)
        
        # 4. Generate the answer
        print("\n" + "="*50)
        answer = ask_llm(user_question, relevant_chunks)
        print("\n[AI RESPONSE]:")
        print(answer)
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Pipelinsre failed: {e}")