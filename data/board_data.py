import json
import requests
from config import CollectionID


async def fetch_board_data():

    try:
        board_query = f"""
                query MyQuery {{
                collections(id: "{CollectionID}") {{
                    nodes {{
                        floorPrice
                        averagePrice
                    }}
                }}
            }}
            """
    except Exception as e:
        print(f"Error fetching board data: {e}")
        return

    result = fetch_graphql(board_query, "MyQuery")
    stats = result['data']['collections']['nodes'][0]

    return stats


async def fetch_nft_data():
    return


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