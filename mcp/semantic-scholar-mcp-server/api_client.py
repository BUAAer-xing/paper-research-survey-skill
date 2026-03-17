import os
from typing import Any
import httpx

BASE_URL = "https://ai4scholar.net"
GRAPH_API = f"{BASE_URL}/graph/v1"
RECOMMENDATIONS_API = f"{BASE_URL}/recommendations/v1"

def _get_api_key() -> str:
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")
    if not key:
        raise ValueError("SEMANTIC_SCHOLAR_API_KEY environment variable is not set")
    return key

def _get_headers(content_type: bool = False) -> dict:
    headers = {"Authorization": f"Bearer {_get_api_key()}"}
    if content_type:
        headers["Content-Type"] = "application/json"
    return headers

async def api_get(url: str, params: dict = None) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=_get_headers(), params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def api_post(url: str, json_body: dict, params: dict = None) -> dict[str, Any] | list | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, headers=_get_headers(content_type=True),
                params=params, json=json_body, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
