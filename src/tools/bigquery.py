from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import os

# Initialize Client (Assumes credentials are set in env or default)
# We will lazy load or initialize globally. 
# For ADK, tools are often simple functions.

class BigQueryTool:
    def __init__(self, project_id: str = None):
        self.client = bigquery.Client(project=project_id)

    def list_datasets(self):
        """Lists all datasets in the project."""
        try:
            datasets = list(self.client.list_datasets())
            return [dataset.dataset_id for dataset in datasets]
        except Exception as e:
            return f"Error listing datasets: {str(e)}"

    def list_tables(self, dataset_id: str):
        """Lists all tables in a specific dataset."""
        try:
            tables = list(self.client.list_tables(dataset_id))
            return [table.table_id for table in tables]
        except Exception as e:
            return f"Error listing tables in {dataset_id}: {str(e)}"

    def get_table_schema(self, dataset_id: str, table_id: str):
        """Returns the schema of a table as a formatted string."""
        try:
            table_ref = self.client.dataset(dataset_id).table(table_id)
            table = self.client.get_table(table_ref)
            schema_info = []
            for schema_field in table.schema:
                schema_info.append(f"{schema_field.name} ({schema_field.field_type}): {schema_field.description or ''}")
            return "\n".join(schema_info)
        except Exception as e:
            return f"Error getting schema for {dataset_id}.{table_id}: {str(e)}"

    def run_query(self, sql_query: str):
        """Executes a SQL query and returns the results."""
        try:
            # Safety check: simplistic 'dry run' could be added here
            query_job = self.client.query(sql_query)
            results = query_job.result()
            
            # Convert to list of dicts for easy consumption by LLM
            rows = [dict(row) for row in results]
            
            # Limit results to avoid context window overflow (e.g., 50 rows)
            # The agent should refine query if it needs more.
            return rows[:50] 
        except GoogleAPIError as e:
            return f"BigQuery API Error: {str(e)}"
        except Exception as e:
            return f"Execution Error: {str(e)}"
