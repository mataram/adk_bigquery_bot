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

    # Load system instruction from file
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_instruction = f.read()

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
