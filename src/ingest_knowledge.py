import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from src.tools.rag import RAGTool

load_dotenv()

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "embedded_knowledges")

def ingest_data():
    """Ingest all text files from the embedded_knowledges folder into ChromaDB."""
    print("Initializing RAG Tool...")
    rag = RAGTool()
    
    # Ensure knowledge directory exists
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)
        print(f"Created knowledge directory: {KNOWLEDGE_DIR}")
        print("Please add .txt files to this folder and run again.")
        return
    
    # Find all .txt files in the knowledge directory
    txt_files = glob.glob(os.path.join(KNOWLEDGE_DIR, "*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {KNOWLEDGE_DIR}")
        print("Please add .txt files to this folder and run again.")
        return
    
    print(f"Found {len(txt_files)} knowledge file(s)")
    
    all_documents = []
    all_ids = []
    
    for file_path in txt_files:
        file_name = Path(file_path).stem
        print(f"  Reading: {Path(file_path).name}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Split by double newlines to create chunks, or use whole file if small
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        
        if not chunks:
            chunks = [content]
        
        for i, chunk in enumerate(chunks):
            doc_id = f"{file_name}_{i}"
            all_documents.append(chunk)
            all_ids.append(doc_id)
    
    print(f"\nIngesting {len(all_documents)} document chunks...")
    result = rag.add_documents(all_documents, all_ids)
    print(result)

if __name__ == "__main__":
    ingest_data()
