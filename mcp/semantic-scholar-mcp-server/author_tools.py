from mcp.server.fastmcp import FastMCP
from api_client import GRAPH_API, api_get, api_post
from credit_tracker import tracker


def register_author_tools(mcp: FastMCP):

    @mcp.tool()
    async def search_authors(query: str, limit: int = 10) -> str:
        """Search for authors by name.

        Args:
            query: Author name to search
            limit: Max results (default 10)
        """
        if not query.strip():
            return "Please provide an author name."
        tracker.record("search_authors")
        url = f"{GRAPH_API}/author/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "authorId,name,paperCount,citationCount,hIndex"
        }
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No authors found."
        lines = [f"Found {len(data['data'])} authors:\n"]
        for author in data['data']:
            lines.append(
                f"- {author.get('name', 'N/A')} | "
                f"Papers: {author.get('paperCount', 'N/A')} | "
                f"Citations: {author.get('citationCount', 'N/A')} | "
                f"h-index: {author.get('hIndex', 'N/A')} | "
                f"ID: {author.get('authorId', 'N/A')}"
            )
        return "\n".join(lines)

    @mcp.tool()
    async def get_author_details(author_id: str) -> str:
        """Get detailed information about an author.

        Args:
            author_id: Author ID
        """
        tracker.record("get_author_details")
        url = f"{GRAPH_API}/author/{author_id}"
        data = await api_get(url)
        if not data:
            return "Unable to fetch author details."
        parts = [
            f"Name: {data.get('name', 'N/A')}",
            f"Papers: {data.get('paperCount', 'N/A')}",
            f"Citations: {data.get('citationCount', 'N/A')}",
            f"h-index: {data.get('hIndex', 'N/A')}",
        ]
        if data.get('homepage'):
            parts.append(f"Homepage: {data['homepage']}")
        if data.get('affiliations'):
            parts.append(f"Affiliations: {', '.join(data['affiliations'])}")
        return "\n".join(parts)

    @mcp.tool()
    async def get_author_papers(author_id: str, limit: int = 20) -> str:
        """Get papers published by an author.

        Args:
            author_id: Author ID
            limit: Max results (default 20)
        """
        tracker.record("get_author_papers")
        url = f"{GRAPH_API}/author/{author_id}/papers"
        params = {
            "limit": limit,
            "fields": "paperId,title,year,citationCount,venue"
        }
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No papers found."
        lines = [f"Found {len(data['data'])} papers:\n"]
        for paper in data['data']:
            lines.append(
                f"- {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')}) "
                f"[citations: {paper.get('citationCount', 'N/A')}]"
            )
        return "\n".join(lines)

    @mcp.tool()
    async def get_authors_batch(author_ids: list[str]) -> str:
        """Get details for multiple authors at once.

        Args:
            author_ids: List of author IDs
        """
        if not author_ids:
            return "Please provide author IDs."
        tracker.record("get_authors_batch")
        url = f"{GRAPH_API}/author/batch"
        data = await api_post(url, {"ids": author_ids})
        if not data:
            return "Unable to fetch authors."
        lines = [f"Fetched {len(data)} authors:\n"]
        for author in data:
            if author:
                lines.append(
                    f"- {author.get('name', 'N/A')} | "
                    f"Papers: {author.get('paperCount', 'N/A')} | "
                    f"h-index: {author.get('hIndex', 'N/A')}"
                )
        return "\n".join(lines)
