from google.cloud import bigquery
import os

def verify_connection():
    print("Attempting to connect to BigQuery...")
    try:
        # Client will attempt to use GOOGLE_APPLICATION_CREDENTIALS or gcloud default auth
        client = bigquery.Client()
        print("Client initialized. Running test query...")
        
        # Public dataset query
        query = """
            SELECT airline_name 
            FROM `bigquery-samples.airline_ontime_data.airline_id_codes` 
            LIMIT 1
        """
        query_job = client.query(query)
        results = query_job.result()
        
        for row in results:
            print(f"SUCCESS: Connected to BigQuery. Found airline: {row.airline_name}")
            return True
            
    except Exception as e:
        print(f"FAILURE: Could not connect to BigQuery.\nError: {e}")
        return False

if __name__ == "__main__":
    verify_connection()
