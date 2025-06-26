from mcp.server.fastmcp import FastMCP
from typing import Dict, List
import logging
import requests

# Create an MCP server
mcp = FastMCP("Giter Fragrance")
logging.basicConfig(level=logging.INFO)

# Add an addition tool
@mcp.tool()
def get_all_fragrances() -> List[Dict[str, str]]:

    """Get all fragrances from the API Giter World"""
    logging.info("MCP: Get all fragrances from the API Giter World")
    b = {
        "productType": "fragrance",
        "volume": ["50"]
    }
    r = requests.post("https://api.giter.world/api/v3/goods/filter", json=b)
    if r.status_code != 200:
        logging.error(f"Failed to get fragrances: {r.status_code}")
        return []

    data = r.json()
    result = []
    for item in data:
        str_item = {k: str(v) for k, v in item.items()}
        result.append(str_item)

    logging.info("MCP: get_all_fragrances: done")
    return result


# Add a dynamic greeting resource
@mcp.resource("greeting://{_id}")
def get_fragrance_by_id(_id: str) -> Dict[str, str]:
    """Get a personalized greeting"""
    logging.info(f"MCP: Get a personalized greeting for {_id}")
    r = requests.get(f"https://api.giter.world/api/v3/goods/product/{_id}")
    logging.info("MCP: get_fragrance_by_id: done")
    return r.json()
