import json
import requests


async def fetch_board_data():

    board_query = """
    query MyQuery {
        collections(id: "0e8e33630d554702a1619418269808b4") {
        nodes {
            floorPrice
            averagePrice
        }
        }
    }
    """

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

    print(response.json())
    return response.json()
