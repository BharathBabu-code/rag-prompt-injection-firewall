#  RAG Prompt Injection Firewall & Security Middleware

A dual-phase, zero-trust security middleware designed to protect Retrieval-Augmented Generation (RAG) applications from direct prompt injections, role confusion attacks, and vector data poisoning. 

By combining **fast heuristic signature matching** with a **local semantic AI guardrail**, this project intercepts and sanitizes malicious payloads at both the user query layer and the retrieved document layer *before* they reach the main inference LLM.

---

##  Architecture & Security Pipeline

Standard RAG architectures blindly append retrieved vector data into the LLM system context, leaving them vulnerable to **Indirect Prompt Injection** (where an attacker embeds malicious instructions inside uploaded documents). 

This firewall enforces a **Zero-Trust Retrieval Pipeline**:

**1.  User Query / Vector Chunks**
⬇
**2.  Phase 1: RegEx Engine**
* **Match:** Redact payload, log the attack, and exit early.
* **Pass:** Move to the next layer.
⬇
**3.  Phase 2: Local LLM Audit**
* **Malicious:** Redact payload.
* **Clean:** Sanitize and continue.
⬇
**4.  FAISS Vector Retrieval**
⬇
**5.  Safe LLM Context Assembly**
⬇
**6.  Final Answer Generation**
└──────────────────────────┘


---

## ✨ Key Features

* **Dual-Phase Defensive Middleware:**
  * **Phase 1 (Heuristic Engine):** Fast RegEx signature scanning for known attack patterns (e.g., system prompt overrides, developer mode toggles, exfiltration hooks). Operates with minimal execution latency (<5ms).
  * **Phase 2 (Semantic AI Guardrail):** Converts complex or obfuscated payloads (such as leetspeak or psychological roleplay overrides) into a semantic classification task handled by a local `mistral` model enforcing strict JSON schema outputs.
* **In-Context Data Sanitization:** Intercepts FAISS vector search results and redacts malicious payloads before appending them to the system instruction prompt.
* **Interactive CLI Comparison Mode:** Features an interactive dashboard allowing developers to run side-by-side comparisons of queries executed **with** the firewall enabled vs. **unprotected raw RAG execution**.
* **Audit Tracing & Security Logging:** Centralized logging module that writes matched threat signatures, attack types, and AI classification reasoning to `logs/security_events.log`.
* **Fail-Safe Exception Handling:** Defaults to restricted access upon guardrail runtime errors or JSON parsing failures, ensuring continuous security boundary enforcement.

---

## 📂 Project Structure

```text
rag-firewall/
├── data/                  # Sample PDF/TXT documents for ingestion
├── logs/                  # Security event logs and threat tracebacks
├── src/
│   ├── ai_detector.py     # Phase 2: Local LLM semantic audit engine
│   ├── detector.py        # Phase 1: RegEx heuristic engine & middleware coordinator
│   ├── ingest.py          # Document parsing, chunking, and FAISS indexing
│   ├── retrieve.py        # Vector search, chunk sanitization, and LLM inference
│   ├── logger.py          # Centralized threat event logging
│   └── main.py            # CLI entry point with interactive comparison dashboard
├── requirements.txt       # Python dependencies
└── README.md              # Documentation


Usage

Launch the interactive CLI dashboard:
Bash

python src/main.py



Workflow Options:

    . Load & Embed Document: Select a PDF/TXT file to chunk, vectorize, and index inside FAISS.

    . Ask AI Question (Comparison Mode):

        Mode 1 (Standard with Firewall): Routes both user input and retrieved chunks through the dual-phase security engine before LLM generation.

        Mode 2 (Raw Query - Unprotected): Bypasses the firewall to demonstrate how vulnerable RAG pipelines execute malicious prompts.

    . View Security Logs: Inspect real-time threat interception logs and AI guardrail reasoning.