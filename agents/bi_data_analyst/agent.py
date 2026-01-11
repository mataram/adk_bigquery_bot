import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk import Agent

# Ensure src is in path if needed, but imports should work if PYTHONPATH is root
from src.tools.bigquery import BigQueryTool
from src.tools.research import ResearchTool
from src.tools.rag import RAGTool

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def create_agent():
    # Configure API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY environment variable not set.")
        # We might not want to crash here if importing, but it is safer to fail fast.
        # However, for CLI, maybe better to just log.
    else:
        genai.configure(api_key=api_key)

    # Initialize Tools
    bq_tool = BigQueryTool()
    research_tool = ResearchTool()
    rag_tool = RAGTool()

    tools_list = [
        bq_tool.list_datasets,
        bq_tool.list_tables,
        bq_tool.get_table_schema,
        bq_tool.run_query,
        research_tool.web_search,
        rag_tool.search
    ]

    system_instruction = """
    You are a Business Intelligence and Data Analyst Chatbot.
    Your goal is to answer user questions using data from BigQuery, external research, or your knowledge base.
    
    Process:
    1. Understand the user's question.
    2. detailed analysis of the question and decide which tool to use.
    3. IF the question is about data/metrics:
       a. List datasets/tables to find relevant data.
       b. Get the schema of relevant tables.
       c. Write and execute a SQL query.
       d. Analyze the results and answer the user.
    4. IF the question requires external context:
       a. Use the web_search tool.
    5. IF the question is about domain knowledge:
       a. Use the knowledge_base search tool.
    
    Always be helpful, concise, and professional.
    When generating SQL, use standard BigQuery SQL syntax.
    """

    # Get model from environment
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    
    agent = Agent(
        name="bi_data_analyst",
        description="A BI Analyst bot capable of SQL generation and Research.",
        model=model_name, 
        instruction=system_instruction,
        tools=tools_list
    )
    
    return agent

# The ADK CLI looks for 'root_agent'
root_agent = create_agent()
