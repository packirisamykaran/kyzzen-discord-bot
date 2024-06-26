
# pylint: disable=import-error

import requests
from typing import Optional, Dict, Any
import aiohttp
import json


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
                     "volumeUsdPast24h", "volumeUsdPast7d", "volumeUsdPast30d", "volumeUsdPast1h", "SOL"}

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
            metrics {{
            nodes {{
                tps
                solUSD
                }}
            }}
        }}
    """
    try:
        result = fetch_graphql(query, "MyQuery")

        stats = result['data']['collections']['nodes'][0]

        stats["TPS"] = result['data']['metrics']['nodes'][0]['tps']
        stats["SOL"] = result['data']['metrics']['nodes'][0]['solUSD']
        stats["raffles"] = 0
        # await fetch_loan_offers("Mad Lads")

        laon_stats = await fetch_loan_offers("Mad Lads")
        stats["loan"] = laon_stats['highest_offer']

        return stats
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
                    volumeUsdPast1h
                    volumeUsdPast24h
                    volumeUsdPast7d
                    volumeUsdPast30d

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


async def get_sol_USD_price():
    sol_price = 0
    async with aiohttp.ClientSession() as session:
        async with session.get("https://price.jup.ag/v4/price?ids=SOL&vsToken=USDC") as response:
            if response.status == 200:
                sol_price = await response.json()  # This gets the JSON content of the response
    return sol_price['data']['SOL']['price']


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


async def fetch_raffles(collection_id: str) -> Optional[Dict[str, Any]]:
    """Fetches board data for the specified collection ID."""
    query = f"""
        query {{
            raffle(collectionId: "{collection_id}") {{
                nodes {{
                    creators
                    howRareRank
                    name
                    moonrankRank
                    endDate
                    price
                    supply
                    sold
                    link
                    createdAt
                    source
                }}
            }}
        }}
    """

    try:
        result = fetch_graphql(query, "MyQuery")

        return result['data']['raffle']['nodes']
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")


async def fetch_loan_offers(collection_name: str) -> Optional[Dict[str, Any]]:
    """Fetches loan offers for the specified collection name."""
    query = f"""
        query {{
            lendingPools(collectionName: "{collection_name}") {{
                nodes {{
                    id
                    collectionName
                    collectionKey
                    lowestOffer
                    availableLiquidity
                    depositYieldApy
                    duration
                    highestOffer
                    interestRate
                    lastLoan
                    ltv
                    marketplace
                    minInterestRate
                    minYieldApy
                    thumbnailUrl
                    totalLiquidity
                }}
            }}
        }}
    """

    try:
        result = fetch_graphql(query, "MyQuery")
        list_of_loans = result['data']['lendingPools']['nodes']

        # iterate and return the data which contains the highest offer out of the list of loans
        highest_offer = 0
        highest_offer_loan = None
        for loan in list_of_loans:
            if loan['highestOffer'] > highest_offer:
                highest_offer = loan['highestOffer']
                highest_offer_loan = loan

        id = highest_offer_loan['id']
        print(highest_offer_loan['marketplace'])
        print(highest_offer_loan['highestOffer'])

        query2 = f"""
           query {{
               lendings(id: "{id}") {{
                   nodes {{
                       id
                       offers
                   }}
               }}
           }}
       """

        result2 = fetch_graphql(query2, "MyQuery")

        offers_string = result2['data']['lendings']['nodes'][0]['offers']
        # its in string dict
        offers = json.loads(offers_string)

        # {'Pubkey': 'DtmgnBCmXpNLqkygj1rP7jRMrCxXbgEXRCjKYZgNf4Vc', 'PrincipalLamports': 100000000, 'OrderBook': '14tngHvcSm4NySKmeDrM2G1bb9QBcVXCtpD9Vt5nKZ1Z', 'IsOffer': True, 'LoanTaken': 0, 'Apy': 18000, 'Apr': 12234, 'Duration': 604800}
        # iterate throuhg the offers and get highest principal lamports
        highest_loan = {}
        for offer in offers:
            if offer['PrincipalLamports'] > highest_loan.get('PrincipalLamports', 0):
                highest_loan = offer

        return_data = {

        }

        return_data['highest_offer'] = f"{highest_loan['PrincipalLamports']/1e9:.2f} SOL"
        return_data['apy'] = f"{highest_loan['Apy']/100:.2f}% APY"
        # over duration to days as whole number
        return_data['duration'] = f"{highest_loan['Duration']/86400:.0f} Days"
        return_data['marketplace'] = highest_offer_loan['marketplace']

        if highest_offer_loan['marketplace'] == "Sharky":
            return_data['link'] = "https://sharky.fi/borrow"
        if highest_offer_loan['marketplace'] == "Citrus":
            return_data['link'] = "https://citrus.famousfoxes.com/borrow"
        if highest_offer_loan['marketplace'] == "Banx":
            return_data['link'] = "https://banx.gg/borrow"

        return return_data
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
