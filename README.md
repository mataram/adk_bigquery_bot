# BI & Data Analyst Chatbot

A Business Intelligence chatbot built with **Google ADK** that can query BigQuery, perform deep research, and use a local knowledge base.

## Features
- **BigQuery Integration**: Query airline flight data
- **Deep Research**: Gemini Deep Research Agent for comprehensive web research (takes 1-5 minutes)
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
   - Add your `GOOGLE_API_KEY`, `GEMINI_MODEL`, `DEEP_RESEARCH_AGENT`, `DEEP_RESEARCH_TIMEOUT`
   - Run `gcloud auth application-default login` for BigQuery

3. **Ingest Knowledge Base** (optional):
   ```bash
   python src/ingest_knowledge.py
   ```

4. **Run the Chatbot**:
   ```bash
   # Windows
   ./run_app.bat
   
   # Linux/Mac
   chmod +x run_app.sh
   ./run_app.sh
   ```
   Open **http://localhost:8000** in your browser.

## Configuration .env file

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API key | Required |
| `GEMINI_MODEL` | LLM model name | `gemini-2.5-pro` |
| `DEEP_RESEARCH_AGENT` | Research agent | `deep-research-pro-preview-12-2025` |
| `DEEP_RESEARCH_TIMEOUT` | Research timeout (seconds) | `120` |

## Project Structure
```
agents/bi_data_analyst/
  ├── agent.py        # ADK Agent definition
  └── prompt.txt      # System prompt (editable)
src/tools/
  ├── bigquery.py     # BigQuery queries
  ├── research.py     # Gemini Deep Research
  └── rag.py          # ChromaDB knowledge base
```
