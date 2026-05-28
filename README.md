# 🏗️ L&T Project Intelligence Copilot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-green.svg)](https://python.langchain.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Serverless-black.svg)](https://www.pinecone.io/)

**Project Intelligence Copilot** is an enterprise-grade Generative AI application designed to act as a proactive control tower for heavy infrastructure projects. By ingesting unstructured project data (Contracts, BOQs, Meeting Minutes, and Vendor Emails) into a vector database, it utilizes a hallucination-resistant Retrieval-Augmented Generation (RAG) pipeline to instantly identify project delays, calculate risk scores, and recommend mitigation actions based on exact contract clauses.

---

## 📸 System Showcase

### 🎥 MVP System Demonstration
The interactive player below demonstrates the end-to-end telemetry and multi-hop reasoning capabilities of the Copilot engine processing real-time project queries:

<p align="center">
  <video src="https://github.com/user-attachments/assets/623d1ff1-ce36-4444-b2a3-b9d31711ad63" width="100%" autoplay muted loop controls>
    Your browser does not support the video tag.
  </video>
</p>

### 1. The Control Tower Interface (Streamlit Frontend)
> Renders complex multi-hop reasoning chains, programmatic risk matrix scores, and explicit context/evidence citations mapped back to foundational documentation.
![Frontend Dashboard](docs/frontend_output.png)

### 2. High-Dimensional Vector Space (Pinecone Serverless)
> Operational view of the 1536-dimensional dense vector space. Chunks are generated via optimized recursive text-splitting configurations and indexed seamlessly for sub-second similarity lookups.
![Pinecone Database](docs/pinecone_db.png)

### 3. Deterministic Guardrails & CI/CD (Pytest Integration)
> Robust validation pipeline enforcing rigid Pydantic schemas. This configuration guarantees predictable JSON payloads, strictly bounded structural integrity, and structural immunity against LLM hallucinations.
![Test Cases](docs/test_cases.png)

---

## 🧠 System Architecture

The core runtime decouples the presentation layer from the asynchronous data ingestion pipeline and the core AI orchestration framework, ensuring modular scalability and low-latency execution boundaries.

```text
=======================================================================================
                   L&T PROJECT INTELLIGENCE COPILOT - ARCHITECTURE
=======================================================================================

[ 1. CLIENT & API SERVICE LAYER ]
      +------------------------+
      |  Customer Dashboard /  |  <-- (Streamlit UI Presentation Layer)
      |  Project Control Tower |
      +-----------+------------+
                  | Asynchronous JSON POST /ask
                  v
      +------------------------+
      |   FastAPI Backend      |  <-- (Uvicorn Gateway, Input Sanitization, Rate Limiting)
      |   (REST API Routing)   |
      +-----------+------------+
                  |
==================|====================================================================
                  v
[ 2. ORCHESTRATION & AGENTIC REASONING LAYER (LangChain LCEL) ]

      +------------------------+       +------------------------------------+
      |  Query Deconstruction  | ----> |  Pydantic Schema Guardrails        |
      |   & Intent Parsing     |       |  (Output Determinism Validation)   |
      +-----------+------------+       +------------------------------------+
                  |                                     ^
                  v                                     | (Enforces Strict JSON Contracts)
      +------------------------+       +----------------+-------------------+
      |  Dense Vector Retriever|       |  Autonomous LLM Reasoning Engine   |
      |   (Cosine Similarity)  | ====> |  (Stateful OpenAI Orchestration)   |
      +-----------+------------+       +------------------------------------+
                  | Query Top-K Chunks                  ^
==================|=====================================|==============================
                  v                                     |
[ 3. ASYNCHRONOUS DATA PIPELINE & MEMORY LAYER ]        |
                                                        |
      +------------------------+                        |
      |  Vector Database       | -----------------------+ (Provides Verified Context 
      |  (Pinecone Serverless) |                           & Metadata Payload)
      +-----------+------------+
                  ^
                  | (High-Throughput Vector Upserts)
      +------------------------+
      |  Embedding Generation  |  <-- (OpenAI text-embedding-3-small | 1536 Dimensions)
      +-----------+------------+
                  ^
                  | (Downstream Semantic Tokens)
      +------------------------+
      | Document Preprocessing |  <-- (PyPDFLoader, RecursiveCharacterTextSplitter)
      |  & Ingestion Pipeline  |
      +-----------+------------+
                  ^
                  | (Source Artifacts Stream)
      [ Raw L&T Project Documents (Contracts, BOQs, MOMs, Safety Reports) ]
