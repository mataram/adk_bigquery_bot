from duckduckgo_search import DDGS
import logging
import os

logger = logging.getLogger(__name__)

class ResearchTool:
    def __init__(self):
        self.ddgs = DDGS()
        self.region = os.getenv("SEARCH_REGION", "wt-wt")

    def web_search(self, query: str, max_results: int = 5) -> str:
        """
        Performs a web search using DuckDuckGo and returns formatted results.
        
        Args:
            query: The search query string.
            max_results: Maximum number of results to return (default 5).
            
        Returns:
            A formatted string containing search results with titles, URLs, and snippets.
        """
        try:
            logger.info(f"Searching for: {query}")
            results = list(self.ddgs.text(query, region=self.region, max_results=max_results))
            logger.info(f"Raw results: {results}")
            
            if not results:
                return f"No search results found for: '{query}'. Try a different query."
            
            # Format results for better LLM consumption
            formatted = []
            for i, r in enumerate(results, 1):
                title = r.get('title', 'No Title')
                href = r.get('href', r.get('link', 'No URL'))
                body = r.get('body', r.get('snippet', 'No description'))
                formatted.append(f"Result {i}:\nTitle: {title}\nURL: {href}\nSummary: {body}")
            
            output = "\n\n".join(formatted)
            logger.info(f"Formatted output: {output[:500]}...")  # Log first 500 chars
            return output
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return f"Search Error: {str(e)}. Please try a simpler query."
