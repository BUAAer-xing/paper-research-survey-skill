from mcp.server.fastmcp import FastMCP
from api_client import GRAPH_API, RECOMMENDATIONS_API, api_get, api_post
from credit_tracker import tracker


def register_recommendation_tools(mcp: FastMCP):

    @mcp.tool()
    async def search_snippets(query: str, limit: int = 5) -> str:
        """Search for relevant text snippets from papers.

        Args:
            query: Search query
            limit: Max results (default 5)
        """
        if not query.strip():
            return "Please provide a query."
        tracker.record("search_snippets")
        url = f"{GRAPH_API}/snippet/search"
        params = {"query": query, "limit": limit}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No snippets found."
        lines = [f"Found {len(data['data'])} snippets:\n"]
        for snippet in data['data']:
            text = snippet.get('text', '')[:500]
            lines.append(f"- {text}")
        return "\n".join(lines)

    @mcp.tool()
    async def get_recommendations_for_paper(paper_id: str, limit: int = 10) -> str:
        """Get paper recommendations based on a single paper.

        Args:
            paper_id: Paper ID to get recommendations for
            limit: Max results (default 10)
        """
        tracker.record("get_recommendations_for_paper")
        url = f"{RECOMMENDATIONS_API}/papers/forpaper/{paper_id}"
        params = {
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount"
        }
        data = await api_get(url, params)
        if not data or not data.get('recommendedPapers'):
            return "No recommendations found."
        papers = data['recommendedPapers']
        lines = [f"Recommended {len(papers)} papers:\n"]
        for paper in papers:
            authors = ', '.join([a.get('name', '') for a in paper.get('authors', [])[:3]])
            lines.append(
                f"- {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')}) "
                f"by {authors} [citations: {paper.get('citationCount', 'N/A')}]"
            )
        return "\n".join(lines)

    @mcp.tool()
    async def get_recommendations_bulk(positive_paper_ids: list[str], negative_paper_ids: list[str] = None, limit: int = 10) -> str:
        """Get paper recommendations based on positive and negative examples.

        Args:
            positive_paper_ids: List of paper IDs you like
            negative_paper_ids: List of paper IDs you don't like (optional)
            limit: Max results (default 10)
        """
        if not positive_paper_ids:
            return "Please provide at least one positive paper ID."
        tracker.record("get_recommendations_bulk")
        url = f"{RECOMMENDATIONS_API}/papers/"
        body = {
            "positivePaperIds": positive_paper_ids,
            "negativePaperIds": negative_paper_ids or [],
            "fields": "paperId,title,authors,year,citationCount"
        }
        data = await api_post(url, body)
        if not data or not data.get('recommendedPapers'):
            return "No recommendations found."
        papers = data['recommendedPapers']
        lines = [f"Recommended {len(papers)} papers:\n"]
        for paper in papers:
            lines.append(
                f"- {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')}) "
                f"[citations: {paper.get('citationCount', 'N/A')}]"
            )
        return "\n".join(lines)
