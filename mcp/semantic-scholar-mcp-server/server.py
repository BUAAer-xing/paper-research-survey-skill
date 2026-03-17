import sys
from mcp.server.fastmcp import FastMCP
from credit_tracker import tracker

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

mcp = FastMCP("semantic-scholar")

# Register all tools
from paper_tools import register_paper_tools
from author_tools import register_author_tools
from recommendation_tools import register_recommendation_tools

register_paper_tools(mcp)
register_author_tools(mcp)
register_recommendation_tools(mcp)


@mcp.tool()
async def get_credit_usage() -> str:
    """Get a summary of API credit usage for this session, including total credits consumed, per-tool breakdown, and recent call history."""
    return tracker.summary()


@mcp.tool()
async def reset_credit_usage() -> str:
    """Reset the credit usage counter to zero."""
    tracker.reset()
    return "Credit usage has been reset."


if __name__ == "__main__":
    mcp.run(transport='stdio')
