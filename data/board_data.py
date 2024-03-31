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

    # madladsresult = await fetchCollectionData()
    results = await fetchFloorPrice()
    print(results)

    return stats


async def fetchFloorPrice():
    try:
        board_query = f"""
                query MyQuery {{
                collections(id: "{CollectionID}") {{
                    nodes {{
                        floorPrice
                    }}
                }}
            }}
            """
    except Exception as e:
        print(f"Error fetching board data: {e}")
        return

    result = fetch_graphql(board_query, "MyQuery")
    stats = result['data']['collections']['nodes'][0]
    return stats['floorPrice']


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


async def fetchCollectionData():
    # GraphQL endpoint
    url = 'https://v8lkzf4yd2.execute-api.us-east-2.amazonaws.com/go-gql'

    # GraphQL query
    query = """
    query collectionQuery($name: String) {
    collections(name: $name) {
        nodes {
        floorPrice
        name
        id
        verified
        createdAt
        thumbnailUrl
        volumePast24h
        averagePrice
        volumeTotal
        volumePast7d
        volumeModifiedAt
        isCurated
        isDerivative
        isNsfw
        links
        bannerUrl
        items
        description
        disputedMessage
        website
        tiktok
        medium
        youtube
        instagram
        discord
        twitter
        __typename
        }
        __typename
    }
    }
    """

    # Variables
    variables = {
        'name': 'Mad Lads'
    }

    # Request payload
    payload = {
        'operationName': 'collectionQuery',
        'query': query,
        'variables': variables
    }

    # Headers (if needed, like Authorization)
    headers = {
        'Content-Type': 'application/json',
        # 'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # Uncomment and replace YOUR_ACCESS_TOKEN if authorization is needed
    }

    # Sending the request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
    else:
        print(f"Query failed to run with a status code {response}")
