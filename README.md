# BI & Data Analyst Chatbot

A Business Intelligence chatbot built with **Google ADK** that can query BigQuery, search the web, and use a local knowledge base.

## Features
- **BigQuery Integration**: Query airline flight data
- **Web Search**: DuckDuckGo-powered research
- **RAG Knowledge Base**: ChromaDB vector store

## Setup

1. **Install Dependencies**:
   ```bash
   conda create -n bot_bq python=3.11
   conda activate bot_bq
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Add your `GOOGLE_API_KEY`
   - Run `gcloud auth application-default login` for BigQuery

3. **Ingest Knowledge Base** (optional):
   ```bash
   python src/ingest_knowledge.py
   ```

4. **Run the Chatbot**:
   ```bash
   ./run_app.bat
   ```
   Open **http://localhost:8000** in your browser.

## Project Structure
```
agents/bi_data_analyst/    # ADK Agent definition
src/tools/                 # BigQuery, Research, RAG tools
chroma_db/                 # Vector store (gitignored)
```
