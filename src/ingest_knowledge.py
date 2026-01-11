from src.tools.rag import RAGTool
import os
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    print("Initializing RAG Tool...")
    rag = RAGTool()
    
    # Sample Knowledge about "Travel" domain
    documents = [
        "Our travel platform offers flights to over 200 destinations worldwide.",
        "We partner with major airlines like Delta, United, and American Airlines.",
        "Our refund policy allows cancellation up to 24 hours before departure for a full refund.",
        "Premium members get free lounge access and priority boarding.",
        "Contact our support team at support@travelbot.com or call 1-800-TRAVEL-HELP.",
        "The 'Super Saver' deal includes a flight + hotel package with 20% discount.",
        "Baggage allowance is 2 checked bags (23kg each) for international flights."
    ]
    
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    print(f"Ingesting {len(documents)} documents...")
    result = rag.add_documents(documents, ids)
    print(result)

if __name__ == "__main__":
    ingest_data()
