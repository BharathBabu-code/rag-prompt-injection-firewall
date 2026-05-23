# Environment & Dependency Log: RAG-Firewall Project

This document catalogs the underlying system utilities, localized AI infrastructure, and Python libraries installed during the initial workspace setup.

## 1. Linux System Utilities (Ubuntu Layer)
These tools were installed directly into the core Linux subsystem to handle file transfers, decompression, and environment management.

| Utility | Command Used | Functional Purpose |
| :--- | :--- | :--- |
| **`python3`** | `sudo apt install python3` | The core execution runtime engine for our application backend. |
| **`python3-pip`** | `sudo apt install python3-pip` | The package installer for Python, used to download third-party software libraries from the Python Package Index (PyPI). |
| **`python3-venv`** | `sudo apt install python3-venv` | The virtualization tool used to construct an isolated Python directory ("clean room"), keeping project packages from contaminating the system layer. |
| **`curl`** | `sudo apt install curl` | A command-line tool for transferring data over network protocols, utilized here to download the native Ollama installer script. |
| **`zstd`** | `sudo apt install zstd` | Zstandard compression/decompression engine. Required by the Linux system to unpack the highly compressed Ollama binary payload. |

---

## 2. Local AI Infrastructure
Instead of relying on external cloud APIs, these tools host and run large language models (LLMs) locally inside the WSL container.

*   **Ollama:** A lightweight service framework that manages the lifetime, memory allocation, and hardware acceleration of large language models on your machine. It exposes a local port (`localhost:11434`) that software applications can query.
*   **Mistral (7B Model):** A highly efficient 7-billion parameter language model pulled natively through Ollama. It serves as the local intelligence engine responsible for parsing text chunks and evaluating incoming security contexts.

---

## 3. Python Ecosystem Applications (`venv` Clean Room)
These specific packages were installed via `pip` inside the virtual environment to build out the Retrieval-Augmented Generation (RAG) and regex scanning pipelines.

> **Note:** These dependencies reside exclusively within the local `venv/` directory and require the environment to be active (`source venv/bin/activate`) to be called.

### requirements.txt
pypdf2==3.0.1
sentence-transformers==3.0.1
faiss-cpu==1.8.0
numpy==1.26.4
ollama==0.2.1

### Technical Breakdown of Libraries:
*   **`pypdf2` (v3.0.1):** A pure-Python PDF library capable of splitting, merging, and parsing PDF files. In this architecture, it handles extracting raw text strings out of documents so they can be processed by the firewall pipeline.
*   **`sentence-transformers` (v3.0.1):** A framework used to generate dense vector embeddings from plain text. It translates human phrases into high-dimensional geometric coordinates based on semantic meaning.
*   **`faiss-cpu` (v1.8.0):** *Facebook AI Similarity Search*. A specialized, highly optimized vector database that stores text embeddings and performs ultra-fast nearest-neighbor searches in memory to find chunks of data with similar semantic meaning.
*   **`numpy` (v1.26.4):** The fundamental scientific computing package for Python. It provides the underlying multi-dimensional array structures and mathematical processing power used by FAISS and Sentence-Transformers to handle vector math.
*   **`ollama` (v0.2.1):** The official Python SDK wrapper. It provides clean, native Python functions (like `ollama.chat()`) to automatically format JSON-RPC payloads and pipe them directly into the background Ollama daemon running on your system.