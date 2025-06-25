from mcp.server.fastmcp import FastMCP

import requests

# Create an MCP server
mcp = FastMCP("Giter Fragrance")


# Add an addition tool
@mcp.tool()
def get_all_fragrances() -> [dict[str, str]]:
    """Get all fragrances from the API Giter World"""
    b = {
        "productType": "fragrance",
        "volume": ["50"]
    }
    r = requests.post("https://api.giter.world/api/v3/goods/filter", json=b)
    return r.json()


# Add a dynamic greeting resource
@mcp.resource("greeting://{_id}")
def get_fragrance_by_id(_id: str) -> dict[str, str]:
    """Get a personalized greeting"""
    r = requests.get(f"https://api.giter.world/api/v3/goods/product/{_id}")
    return r.json()
