import os
import sys
import ingest
import retrieve
from detector import scan_and_redact

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*60)
    print("RAG PROMPT INJECTION FIREWALL (CLI V1.0)")
    print("="*60)

def menu_load_document():
    filepath = input("\n[?] Enter the path to the document (e.g., data/sample.pdf): ").strip()
    if not os.path.exists(filepath):
        print("[!] File not found. Please check the path.")
        return
    
    print("\n[STARTING INGESTION PIPELINE]")
    raw_text = ingest.read_file_content(filepath)
    clean_text_data = ingest.clean_text(raw_text)
    chunks = ingest.chunk_text(clean_text_data)
    ingest.build_and_save_vector_db(chunks)
    input("\nPress Enter to return to menu...")

def menu_ask_question():
    try:
        index, chunks = retrieve.load_database()
    except FileNotFoundError:
        print("[!] Database not found. Please load a document first.")
        return

    print("\n--- COMPARISON MODE ---")
    print("1. Standard Query (WITH Firewall)")
    print("2. Raw Query (WITHOUT Firewall - Vulnerable!)")
    mode = input("Select mode (1/2): ").strip()

    question = input("\n[?] Enter your question for the AI: ").strip()

    if mode == "1":
        print("\n[🛡️ ROUTING THROUGH SECURITY MIDDLEWARE...]")
        print("[*] Scanning user input for direct prompt injection...")
        safe_question, is_direct_attack = scan_and_redact(question)
        
        if is_direct_attack:
            print("\n[🚨 CRITICAL] Direct Prompt Injection detected in user input!")
            print("[!] Query blocked and logged. Disconnecting session.")
            input("\nPress Enter to return to menu...")
            return
        relevant_chunks = retrieve.search_and_sanitize_chunks(safe_question, index, chunks)
        answer = retrieve.ask_llm(safe_question, relevant_chunks)
    else:
        print("\n[⚠️ WARNING: BYPASSING FIREWALL...]")
        # Bypasses the firewall, simulating a raw, unprotected RAG search
        from sentence_transformers import SentenceTransformer
        import numpy as np
        model = SentenceTransformer('all-MiniLM-L6-v2')
        q_vec = np.array(model.encode([question])).astype('float32')
        _, indices = index.search(q_vec, 3)
        relevant_chunks = [chunks[i] for i in indices[0] if i != -1]

        answer = retrieve.ask_llm(question, relevant_chunks)
    
    print("\n" + "="*50)
    print("[AI RESPONSE]:")
    print(answer)
    print("="*50)
    input("\nPress Enter to return to menu...")

def menu_view_logs():
    log_path = "logs/security_events.log"
    print("\n--- SECURITY EVENT LOGS ---")
    if not os.path.exists(log_path):
        print("No logs found. The system is clean.")
    else:
        with open(log_path, "r") as f:
            for line in f.readlines():
                print(line.strip())
    input("\nPress Enter to return to menu...")

def main():
    while True:
        clear_screen()
        print_header()
        print("1. 📂 Load & Embed Document (PDF/TXT)")
        print("2. 💬 Ask AI Question (Comparison Mode)")
        print("3. 📋 View Security Logs")
        print("4. ❌ Exit")
        print("-" * 60)
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            menu_load_document()
        elif choice == "2":
            menu_ask_question()
        elif choice == "3":
            menu_view_logs()
        elif choice == "4":
            print("\nShutting down firewall... Goodbye!\n")
            sys.exit(0)
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()