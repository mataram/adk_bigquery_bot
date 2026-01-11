import chromadb
import google.generativeai as genai
import os

# Placeholder for RAG Tool
# This requires a valid API key for embeddings to work.
# We will use a local non-persistent client for testing if no path provided.

class RAGTool:
    def __init__(self, collection_name: str = "travel_knowledge", persist_dir: str = "./chroma_db"):
        if persist_dir:
            self.client = chromadb.PersistentClient(path=persist_dir)
        else:
            self.client = chromadb.PersistentClient(path="./chroma_db")
            
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
        # Configure GenAI (assumes API key in env)
        if os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    def add_documents(self, documents: list[str], ids: list[str]):
        """Adds documents to the knowledge base."""
        try:
            # We need to generate embeddings. 
            # For simplicity in this tool, we might rely on Chroma's default or simple embeddings 
            # if GenAI fails, but the plan specified Gemini embeddings.
            
            # Simple embedding via GenAI
            embeddings = []
            for doc in documents:
                # This is a synchronous call, might be slow for batch
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=doc,
                    task_type="retrieval_document",
                    title="Knowledge Doc"
                )
                embeddings.append(result['embedding'])

            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                ids=ids
            )
            return f"Successfully added {len(documents)} documents."
        except Exception as e:
            return f"Error adding documents: {str(e)}"

    def search(self, query: str, n_results: int = 3):
        """Searches the knowledge base."""
        try:
            # Embed query
            result = genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results['documents'][0] # Return list of strings
        except Exception as e:
            return f"RAG Search Error: {str(e)}"
