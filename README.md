# RAG Backend: FastAPI, Qdrant, & Groq (Llama 3.3)

This is a robust Retrieval-Augmented Generation (RAG) backend built with **FastAPI**. It enables document ingestion (PDF/TXT), intelligent chunking, and high-performance vector search using **Qdrant**. The chat interface leverages **Groq's Llama 3.3-70b** for lightning-fast responses and includes automated booking detail extraction.

## Features

- **Document Processing**: Supports PDF and TXT file uploads with automatic text extraction.
- **Chunking Strategies**: Choice between `fixed` and `recursive` chunking for optimal context retrieval.
- **Vector Database**: Uses Qdrant for efficient similarity search.
- **Advanced LLM**: Powered by `llama-3.3-70b-versatile` via Groq.
- **Session Management**: Persistent chat history and booking data storage via Redis.
- **Information Extraction**: Automatically identifies and saves booking details (name, email, date, time) from conversations.

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag_backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and fill in your credentials:
   ```env
   DATABASE_URL=sqlite:///./sql_app.db
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   GROQ_API_KEY=your_groq_api_key
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

5. **Initialize the collection:**
   ```bash
   python -m scripts.create_collection
   ```

6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🛠 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/ingest` | `POST` | Upload PDF/TXT, select chunking strategy, and store in Qdrant. |
| `/chat` | `POST` | Query the RAG system using a `session_id`. Returns AI response and extracted booking data. |

## Project Structure

- `app/api/`: API route definitions (Ingestion & Chat).
- `app/services/`: Core logic for embeddings, document processing, and database clients.
- `uploaded_files/`: Local storage for processed documents (git-ignored).