from mcp.server.fastmcp import FastMCP
from typing import Dict, List
import logging
import requests

# Create an MCP server
mcp = FastMCP("Giter Fragrance")
logging.basicConfig(level=logging.INFO)

# Add an addition tool
@mcp.tool(name="Get-all-fragrances", description="Get all fragrances from the API Giter World")
def get_all_fragrances() -> List[Dict[str, str]]:
    """
    Get a list of all fragrances from the Giter World API.

    This function sends a POST request to the Giter World API to retrieve
    all available fragrances with specific criteria. The results are
    processed and returned as a list of dictionaries containing the
    fragrance details.

    :raises requests.RequestException: If there is an issue making the
        request to the API.
    :raises ValueError: If the response data is not valid JSON.

    :return: A list of dictionaries, where each dictionary contains
        details about a fragrance.
    :rtype: List[Dict[str, str]]
    """
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
@mcp.tool(name="Get-information-by-id", description="Get information about a fragrance by its ID from the API Giter World.")
def get_fragrance_by_id(product_id: str) -> Dict[str, str]:
    """
    Get information about a fragrance by its ID from the API Giter World.

    This function fetches details of a fragrance product by making a GET request to the
    Giter World API based on the given ID. It returns the details of the fragrance in a
    dictionary format containing various attributes.

    :param product_id: The unique identifier of the fragrance product to retrieve from the API.
    :type product_id: str
    :return: A dictionary containing details of the fragrance product fetched from the API.
    :rtype: Dict[str, str]
    """
    logging.info(f"MCP: Get a personalized greeting for {product_id}")
    r = requests.get(f"https://api.giter.world/api/v3/goods/product/{product_id}")
    logging.info("MCP: get_fragrance_by_id: done")
    return r.json()
