# pylint: disable=import-error
import json
import requests
from config import CollectionID


async def fetch_board_data():

    try:
        board_query = f"""
                query MyQuery {{
                collections(id: "{CollectionID}") {{
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

        result = fetch_graphql(board_query, "MyQuery")

        stats = result['data']['collections']['nodes'][0]

        return stats
    except Exception as e:
        print(f"Error fetching board data: {e}")
        return


async def fetchStats(collectionID, stat):
    try:
        board_query = f"""
                query MyQuery {{
                collections(id: "{collectionID}") {{
                    nodes {{
                        {stat}
                    }}
                }}
            }}
            """

    except Exception as e:
        print(f"Error fetching board data: {e}")
        return

    result = fetch_graphql(board_query, "MyQuery")
    stat_result = result['data']['collections']['nodes'][0]
    print(stat_result[stat])
    return format_data(stat, stat_result[stat])


def fetch_graphql(operations_doc, operation_name, variables={}):
    response = requests.post(
        "https://v8lkzf4yd2.execute-api.us-east-2.amazonaws.com/go-gql",
        json={
            "query": operations_doc,
            "variables": variables,
            "operationName": operation_name
        }
    )
    return response.json()


def format_data(stat, value):
    sol_stats = ["floorPrice", "averagePrice", "volumePast24h",
                 "volumePast7d", "volumePast30d", "volumePast1h", "volumeTotal"]
    decimal_stats = ["volumePast7dDelta", "volumePast30dDelta", "volumePast24hDelta", "volumePast1hDelta", "floorPricePast7dDelta", "floorPricePast30dDelta",
                     "floorPricePast24hDelta", "floorPricePast1hDelta", "floorPriceDelta", "averagePriceDelta", "volumeUsdPast24h", "volumeUsdPast7d", "volumeUsdPast30d", "volumeUsdPast1h"]

    if stat in sol_stats and stat not in decimal_stats:
        formatted_value = f"{float(value) / 10**9:.2f}"
    elif stat in decimal_stats:
        formatted_value = f"{float(value):.2f}"
    else:
        formatted_value = value  # No formatting for non-decimal or special cases

    return formatted_value


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
