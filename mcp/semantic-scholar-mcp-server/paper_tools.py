import unicodedata
from mcp.server.fastmcp import FastMCP
from api_client import GRAPH_API, api_get, api_post
from credit_tracker import tracker

def format_paper(data: dict) -> str:
    if not data:
        return "No paper data available"
    try:
        title = unicodedata.normalize('NFKD', str(data.get('title', 'N/A')))
        authors = ', '.join([a.get('name', 'Unknown') for a in data.get('authors', [])])
        year = data.get('year') or 'N/A'
        citation_count = data.get('citationCount', 'N/A')
        venue = data.get('venue') or 'N/A'
        abstract = data.get('abstract') or 'N/A'
        external_ids = data.get('externalIds', {}) or {}
        doi = external_ids.get('DOI', 'N/A')
        pdf_data = data.get('openAccessPdf', {}) or {}
        pdf_url = pdf_data.get('url', 'N/A')
        tldr = (data.get('tldr') or {}).get('text', '')

        parts = [
            f"Title: {title}",
            f"Authors: {authors}",
            f"Year: {year}",
            f"Citations: {citation_count}",
            f"Venue: {venue}",
            f"DOI: {doi}",
            f"PDF: {pdf_url}",
            f"Abstract: {abstract}",
        ]
        if tldr:
            parts.append(f"TL;DR: {tldr}")
        return "\n".join(parts)
    except Exception as e:
        return f"Error formatting paper: {e}"


PAPER_FIELDS = "paperId,title,authors,year,abstract,citationCount,venue,externalIds,isOpenAccess,openAccessPdf,tldr"
PAPER_FIELDS_BRIEF = "paperId,title,authors,year,citationCount"


def register_paper_tools(mcp: FastMCP):

    @mcp.tool()
    async def search_papers(query: str, limit: int = 10) -> str:
        """Search for academic papers by keywords.

        Args:
            query: Search keywords
            limit: Max results (default 10)
        """
        if not query.strip():
            return "Please provide a search query."
        tracker.record("search_papers")
        url = f"{GRAPH_API}/paper/search"
        params = {"query": query[:300], "limit": limit, "fields": PAPER_FIELDS}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No results found."
        results = [f"Found {data.get('total', 0)} papers:\n"]
        for paper in data['data']:
            results.append(format_paper(paper))
        return "\n---\n".join(results)

    @mcp.tool()
    async def search_papers_bulk(query: str, limit: int = 10) -> str:
        """Bulk search papers with complex query syntax (AND/OR/phrases).

        Args:
            query: Complex query (e.g. "machine learning | deep learning")
            limit: Max results (default 10)
        """
        if not query.strip():
            return "Please provide a search query."
        tracker.record("search_papers_bulk")
        url = f"{GRAPH_API}/paper/search/bulk"
        params = {"query": query[:300], "limit": limit, "fields": PAPER_FIELDS}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No results found."
        results = [f"Found {len(data['data'])} papers:\n"]
        for paper in data['data']:
            results.append(format_paper(paper))
        return "\n---\n".join(results)

    @mcp.tool()
    async def match_paper_by_title(title: str) -> str:
        """Match a paper by its exact title.

        Args:
            title: The exact paper title to match
        """
        if not title.strip():
            return "Please provide a title."
        tracker.record("match_paper_by_title")
        url = f"{GRAPH_API}/paper/search/match"
        params = {"query": title, "fields": PAPER_FIELDS}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No matching paper found."
        results = []
        for paper in data['data']:
            results.append(format_paper(paper))
        return "\n---\n".join(results)

    @mcp.tool()
    async def get_autocomplete(query: str) -> str:
        """Get autocomplete suggestions for paper titles/authors.

        Args:
            query: Partial query string
        """
        if not query.strip():
            return "Please provide a query."
        tracker.record("get_autocomplete")
        url = f"{GRAPH_API}/paper/autocomplete"
        params = {"query": query}
        data = await api_get(url, params)
        if not data or not data.get('matches'):
            return "No suggestions found."
        return "\n".join([f"- {m}" for m in data['matches']])

    @mcp.tool()
    async def get_paper_details(paper_id: str) -> str:
        """Get detailed information about a specific paper.

        Args:
            paper_id: Paper ID (Semantic Scholar ID, DOI:xxx, CorpusId:xxx, etc.)
        """
        tracker.record("get_paper_details")
        url = f"{GRAPH_API}/paper/{paper_id}"
        params = {"fields": "paperId,title,authors,year,abstract,citationCount,venue,references,citations,externalIds,isOpenAccess,openAccessPdf,tldr"}
        data = await api_get(url, params)
        if not data:
            return "Unable to fetch paper details."
        return format_paper(data)

    @mcp.tool()
    async def get_paper_authors(paper_id: str) -> str:
        """Get all authors of a specific paper.

        Args:
            paper_id: Paper ID
        """
        tracker.record("get_paper_authors")
        url = f"{GRAPH_API}/paper/{paper_id}/authors"
        data = await api_get(url)
        if not data or not data.get('data'):
            return "No authors found."
        lines = [f"Found {len(data['data'])} authors:\n"]
        for author in data['data']:
            parts = [f"Name: {author.get('name', 'N/A')}"]
            parts.append(f"Author ID: {author.get('authorId', 'N/A')}")
            if author.get('affiliations'):
                parts.append(f"Affiliations: {', '.join(author['affiliations'])}")
            lines.append("\n".join(parts))
        return "\n---\n".join(lines)

    @mcp.tool()
    async def get_paper_citations(paper_id: str, limit: int = 10) -> str:
        """Get papers that cite the specified paper.

        Args:
            paper_id: Paper ID
            limit: Max results (default 10)
        """
        tracker.record("get_paper_citations")
        url = f"{GRAPH_API}/paper/{paper_id}/citations"
        params = {"limit": limit, "fields": PAPER_FIELDS_BRIEF}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No citations found."
        lines = [f"Found {len(data['data'])} citing papers:\n"]
        for item in data['data']:
            paper = item.get('citingPaper') or item
            lines.append(f"- {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')}) [citations: {paper.get('citationCount', 'N/A')}]")
        return "\n".join(lines)

    @mcp.tool()
    async def get_paper_references(paper_id: str, limit: int = 10) -> str:
        """Get references of the specified paper.

        Args:
            paper_id: Paper ID
            limit: Max results (default 10)
        """
        tracker.record("get_paper_references")
        url = f"{GRAPH_API}/paper/{paper_id}/references"
        params = {"limit": limit, "fields": PAPER_FIELDS_BRIEF}
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No references found."
        lines = [f"Found {len(data['data'])} references:\n"]
        for item in data['data']:
            paper = item.get('citedPaper') or item
            lines.append(f"- {paper.get('title', 'N/A')} ({paper.get('year', 'N/A')}) [citations: {paper.get('citationCount', 'N/A')}]")
        return "\n".join(lines)

    @mcp.tool()
    async def get_papers_batch(paper_ids: list[str]) -> str:
        """Get details for multiple papers at once.

        Args:
            paper_ids: List of paper IDs (Semantic Scholar IDs, DOI:xxx, CorpusId:xxx, etc.)
        """
        if not paper_ids:
            return "Please provide paper IDs."
        tracker.record("get_papers_batch")
        url = f"{GRAPH_API}/paper/batch"
        params = {"fields": PAPER_FIELDS}
        data = await api_post(url, {"ids": paper_ids}, params=params)
        if not data:
            return "Unable to fetch papers."
        results = [f"Fetched {len(data)} papers:\n"]
        for paper in data:
            if paper:
                results.append(format_paper(paper))
        return "\n---\n".join(results)

    @mcp.tool()
    async def search_by_topic(topic: str, year_start: int = None, year_end: int = None, limit: int = 10) -> str:
        """Search papers by topic with optional year range filter.

        Args:
            topic: Search topic
            year_start: Start year (optional)
            year_end: End year (optional)
            limit: Max results (default 10)
        """
        if not topic.strip():
            return "Please provide a topic."
        tracker.record("search_by_topic")
        url = f"{GRAPH_API}/paper/search"
        params = {"query": topic[:300], "limit": limit, "fields": PAPER_FIELDS}
        if year_start and year_end:
            params["year"] = f"{year_start}-{year_end}"
        data = await api_get(url, params)
        if not data or not data.get('data'):
            return "No results found."
        results = [f"Found papers on '{topic}':\n"]
        for paper in data['data']:
            results.append(format_paper(paper))
        return "\n---\n".join(results)
