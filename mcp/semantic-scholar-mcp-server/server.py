import logging
import sys
import os
from datetime import datetime
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import unicodedata
import json
import sys

# Set UTF-8 as default encoding for Python
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize FastMCP server
mcp = FastMCP("semantic-scholar")

# Constants
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1"
USER_AGENT = "semantic-scholar-app/1.0"


async def make_api_request(url: str, headers: dict = None, params: dict = None) -> dict[str, Any] | None:
    """Make a request to the API with proper error handling."""
    if headers is None:
        headers = { "User-Agent": USER_AGENT }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

def format_paper_data(data: dict) -> str:
    """Format paper data into a consistent string format."""
    if not data:
        return "No paper data available"

    try:
        title = unicodedata.normalize('NFKD', str(data.get('title', 'No title available')))
        authors = ', '.join([author.get('name', 'Unknown Author') for author in data.get('authors', [])])
        year = data.get('year') or 'Year unknown'
        external_ids = data.get('externalIds', {}) or {}
        doi = external_ids.get('DOI', 'No DOI available')
        venue = data.get('venue') or 'Venue unknown'
        abstract = data.get('abstract') or 'No abstract available'
        tldr = (data.get('tldr') or {}).get('text', '')
        is_open = "Yes" if data.get('isOpenAccess') else "No"
        pdf_data = data.get('openAccessPdf', {}) or {}
        pdf_url = pdf_data.get('url', 'Not available')

        result = [
            f"Title: {title}",
            f"Authors: {authors}",
            f"Year: {year}",
            f"DOI: {doi}",
            f"Venue: {venue}",
            f"Open Access: {is_open}",
            f"PDF URL: {pdf_url}",
            f"Abstract: {abstract}"
        ]
        if tldr:
            result.append(f"TL;DR: {tldr}")

        return "\n".join(result) + "\t\t\n"

    except Exception as e:
        return f"Error formatting paper data: {str(e)}"

@mcp.tool()
async def search_papers(query: str, limit: int = 10) -> str:
    """Search for papers on Semantic Scholar.

    args:
        query: the search query
        limit: the maximum number of results to return (default 10)
    """

    if query == "":
        return "Please provide a search query."

    # Truncate long queries
    MAX_QUERY_LENGTH = 300
    if len(query) > MAX_QUERY_LENGTH:
        query = query[:MAX_QUERY_LENGTH] + "..."

    try:
        semantic_url = f"{SEMANTIC_SCHOLAR_API}/paper/search?query={query}&limit={limit}"
        semantic_data = await make_api_request(semantic_url)

        results = []

        if semantic_data and 'papers' in semantic_data:
            results.append("=== Semantic Scholar Results ===")
            for paper in semantic_data['papers']:
                results.append(format_paper_data(paper))

        if not results:
            return "No results found or error occurred while fetching papers."

        return "\n".join(results)
    except:
        return "Error searching papers."

@mcp.tool()
async def fetch_paper_details(paper_id: str) -> str:
    """Get detailed information about a specific paper.

    Args:
        paper_id: Paper identifier (Semantic Scholar paper ID or DOI)
    """
    url = f"{SEMANTIC_SCHOLAR_API}/paper/{paper_id}"
    data = await make_api_request(url)

    if not data:
        return "Unable to fetch paper details."

    return format_paper_data(data)


@mcp.tool()
async def search_by_topic(topic: str, year_start: int = None, year_end: int = None, limit: int = 10) -> str:
    """Search for papers by topic with optional date range. 
    
    Note: Query length is limited to 300 characters. Longer queries will be automatically truncated.
    
    Args:
        topic (str): Search query (max 300 chars)
        year_start (int, optional): Start year for date range
        year_end (int, optional): End year for date range  
        limit (int, optional): Maximum number of results to return (default 10)
        
    Returns:
        str: Formatted search results or error message
    """
    
    try:
        # Truncate long queries to prevent API errors
        MAX_QUERY_LENGTH = 300
        if len(topic) > MAX_QUERY_LENGTH:
            original_length = len(topic)
            topic = topic[:MAX_QUERY_LENGTH] + "..."
        
        # Try Semantic Scholar API first
        semantic_url = f"{SEMANTIC_SCHOLAR_API}/paper/search"
        params = {
            "query": topic.encode('utf-8').decode('utf-8'),
            "limit": limit,
            "fields": "title,authors,year,paperId,externalIds,abstract,venue,isOpenAccess,openAccessPdf,tldr"
        }
        if year_start and year_end:
            params["year"] = f"{year_start}-{year_end}"
            
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8"
        }
        data = await make_api_request(semantic_url, headers=headers, params=params)
        
        if data and 'data' in data:
            results = ["=== Search Results ==="]
            for paper in data['data']:
                results.append(format_paper_data(paper))
            return "\n".join(results)

        return "No results found or error occurred while fetching papers."
        
    except Exception as e:
        return f"Error searching papers!"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
