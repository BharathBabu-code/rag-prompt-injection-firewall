import os
import re
import json
import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def read_file_content(file_path):
    """Dynamically reads a file based on its extension (.pdf or .txt)."""
    # Check if it's a plain text file
    if file_path.endswith('.txt'):
        print(f"[*] Extracting text from raw text file: {file_path}...")
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
            
    # Check if it's a PDF
    elif file_path.endswith('.pdf'):
        print(f"[*] Extracting text from PDF file: {file_path}...")
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
        return text
    
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

def clean_text(raw_text):
    """Sanitizes messy PDF text by removing weird spacing and broken lines."""
    print("[*] Sanitizing text...")
    # Replace newlines with spaces
    text = re.sub(r'\n', ' ', raw_text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=300, overlap=50):
    """Splits a massive wall of text into smaller, overlapping chunks of words."""
    print(f"[*] Chunking text (Size: {chunk_size} words, Overlap: {overlap} words)...")
    words = text.split()
    chunks = []
    
    # Loop through the words, jumping forward by (chunk_size - overlap)
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        
    print(f"    -> Created {len(chunks)} chunks.")
    return chunks

def build_and_save_vector_db(chunks, db_dir="embeddings"):
    """Converts text chunks to embeddings and saves them to a FAISS index."""
    print("[*] Loading embedding model (all-MiniLM-L6-v2)...")
    # This downloads a small, highly efficient local AI model just for embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("[*] Converting text chunks into mathematical vectors...")
    # Convert chunks to vector coordinates
    embeddings = model.encode(chunks)
    
    # FAISS requires the vectors to be in a specific float32 format
    embeddings = np.array(embeddings).astype('float32')
    
    print("[*] Building FAISS database...")
    # 384 is the specific dimension size outputted by all-MiniLM-L6-v2
    dimension = 384 
    index = faiss.IndexFlatL2(dimension)
    
    # Add our embeddings into the database
    index.add(embeddings)
    
    # Save the FAISS index (the math map)
    faiss.write_index(index, os.path.join(db_dir, "vector_index.faiss"))
    
    # Save the actual text chunks (so we can read what the vectors point to)
    with open(os.path.join(db_dir, "chunks.json"), "w") as f:
        json.dump(chunks, f)
        
    print(f"[SUCCESS] Vector database saved to '{db_dir}/' folder.")

if __name__ == "__main__":
    # Define our target file
    target_file = "attacks/malicious_doc.txt"
    
    if not os.path.exists(target_file):
        print(f"[ERROR] Could not find {target_file}. Please put a PDF in the data folder.")
    else:
        # The Pipeline Execution
        raw_text = read_file_content(target_file)
        clean_text_data = clean_text(raw_text)
        document_chunks = chunk_text(clean_text_data)
        build_and_save_vector_db(document_chunks)