import os
import time
import logging
from google import genai

logger = logging.getLogger(__name__)

class ResearchTool:
    """Research tool using Gemini Deep Research for comprehensive web research."""
    
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
        self.agent = os.getenv("DEEP_RESEARCH_AGENT", "deep-research-pro-preview-12-2025")
        self.timeout = int(os.getenv("DEEP_RESEARCH_TIMEOUT", "120"))  # seconds

    def web_search(self, query: str) -> str:
        """
        Performs comprehensive deep research using Gemini Deep Research Agent.
        
        IMPORTANT: This is a thorough research process that typically takes 1-3 minutes 
        to complete. The agent will browse multiple sources and synthesize findings 
        into a comprehensive report. Please inform the user that research is in progress
        and results will be available shortly.
        
        Args:
            query: The research query string.
            
        Returns:
            A comprehensive research report on the topic with citations.
        """
        try:
            logger.info(f"Starting deep research for: {query}")
            
            # Start the research task
            interaction = self.client.interactions.create(
                input=query,
                agent=self.agent,
                background=True
            )
            
            logger.info(f"Research started with interaction ID: {interaction.id}")
            
            # Poll for results with timeout
            start_time = time.time()
            poll_count = 0
            while True:
                elapsed = time.time() - start_time
                if elapsed > self.timeout:
                    return f"Research timed out after {self.timeout} seconds for query: '{query}'. Try a simpler question."
                
                interaction = self.client.interactions.get(interaction.id)
                poll_count += 1
                
                if poll_count % 6 == 0:  # Every 30 seconds
                    logger.info(f"Still researching... ({int(elapsed)}s elapsed)")
                
                if interaction.status == "completed":
                    result = interaction.outputs[-1].text if interaction.outputs else "No results found."
                    logger.info(f"Research completed. Result length: {len(result)}")
                    return result
                elif interaction.status == "failed":
                    error = getattr(interaction, 'error', 'Unknown error')
                    logger.error(f"Research failed: {error}")
                    return f"Research failed: {error}"
                
                time.sleep(5)  # Poll every 5 seconds
                
        except Exception as e:
            logger.error(f"Deep research error: {e}")
            return f"Research Error: {str(e)}. Please try again."
