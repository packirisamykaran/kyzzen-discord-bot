
# pylint: disable=import-error

import requests
from typing import Optional, Dict, Any


GRAPHQL_ENDPOINT = "https://v8lkzf4yd2.execute-api.us-east-2.amazonaws.com/go-gql"


def fetch_graphql(query: str, operation_name: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executes a GraphQL query and returns the JSON response."""
    if variables is None:
        variables = {}
    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": query, "variables": variables,
              "operationName": operation_name}
    )
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()


def format_data(stat: str, value: Any) -> str:
    """Formats data based on the stat type."""
    sol_stats = {"floorPrice", "averagePrice", "volumePast24h",
                 "volumePast7d", "volumePast30d", "volumePast1h", "volumeTotal"}
    decimal_stats = {"volumePast7dDelta", "volumePast30dDelta", "volumePast24hDelta", "volumePast1hDelta", "floorPricePast7dDelta",
                     "floorPricePast30dDelta", "floorPricePast24hDelta", "floorPricePast1hDelta", "floorPriceDelta", "averagePriceDelta",
                     "volumeUsdPast24h", "volumeUsdPast7d", "volumeUsdPast30d", "volumeUsdPast1h"}

    if stat in sol_stats:
        return f"{float(value) / 1e9:.2f}"
    elif stat in decimal_stats:
        return f"{float(value):.2f}"
    return str(value)  # Return as string for consistency


async def fetch_board_data(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    totalOwners
                    listed
                    floorPrice
                    averagePrice
                    salesPast24h
                    salesPast7d
                    volumePast24h
                    volumePast7d
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        return result['data']['collections']['nodes'][0]
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


async def fetch_volume_data(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    volumePast1h
                    volumePast24h
                    volumePast7d
                    volumePast30d
                    volumeTotal
                    volumePast1hDelta  
                    volumePast24hDelta
                    volumePast7dDelta
                    volumePast30dDelta
            
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        # loop and format the data
        for key, value in result['data']['collections']['nodes'][0].items():
            result['data']['collections']['nodes'][0][key] = format_data(
                key, value)

        return result['data']['collections']['nodes'][0]

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


async def fetch_sales_data(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    salesPast1h
                    salesPast24h
                    salesPast7d
                    salesPast30d
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        return result['data']['collections']['nodes'][0]
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


async def fetch_volume_usd_data(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    volumeUsdPast1h
                    volumeUsdPast24h
                    volumeUsdPast7d
                    volumeUsdPast30d
                    volumePast1hDelta  
                    volumePast24hDelta
                    volumePast7dDelta
                    volumePast30dDelta
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        # loop and format the data
        for key, value in result['data']['collections']['nodes'][0].items():
            result['data']['collections']['nodes'][0][key] = format_data(
                key, value)

        return result['data']['collections']['nodes'][0]

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


async def fetch_floor_price_data(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    floorPrice
                    floorPricePast1hDelta
                    floorPricePast24hDelta
                    floorPricePast7dDelta
                    floorPricePast30dDelta
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        # loop and format the data
        for key, value in result['data']['collections']['nodes'][0].items():
            result['data']['collections']['nodes'][0][key] = format_data(
                key, value)

        return result['data']['collections']['nodes'][0]
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


async def fetch_stats(collection_id: str, stat: str) -> Optional[str]:
    """Fetches a specific stat for the specified collection ID."""
    query = f"""
        query {{
            collections(id: "{collection_id}") {{
                nodes {{
                    {stat}
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")
        stat_result = result['data']['collections']['nodes'][0]
        return format_data(stat, stat_result[stat])
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


# query MyQuery {
#   collections(id: "0e8e33630d554702a1619418269808b4") {
#     nodes {
#       averagePrice
#       averagePriceDelta
#       floorPrice
#       floorPriceDelta
#       floorPricePast7dDelta
#       floorPricePast1hDelta
#       floorPricePast24hDelta
#       floorPricePast30dDelta
#       salesPast1h
#       salesPast24h
#       salesPast30d
#       salesPast7d
#       totalOwners
#       volumePast1h
#       volumePast1hDelta
#       volumePast24hDelta
#       volumePast24h
#       volumePast30d
#       volumePast30dDelta
#       volumePast7d
#       volumePast7dDelta
#       volumeTotal
#       volumeUsdPast1h
#       volumeUsdPast24h
#       volumeUsdPast30d
#       volumeUsdPast7d
#     }
#   }
# }
