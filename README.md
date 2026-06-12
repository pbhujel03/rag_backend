# RAG Backend with FastAPI, Qdrant, and Groq

A Retrieval-Augmented Generation (RAG) system that allows you to upload documents (PDF/TXT), chunk them, store them in a Qdrant vector database, and chat with them using Llama 3 on Groq.

## Setup

1. **Clone the repository**
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
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite:///./sql_app.db
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   GROQ_API_KEY=your_groq_api_key
   ```
5. **Initialize the collection:**
   ```bash
   python -m scripts.create_collection
   ```
6. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```