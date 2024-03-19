import json


async def fetch_nft_data():

    # Load data from data.json
    with open('data.json', 'r') as f:
        data = json.load(f)

    total_listed = data["Total Listed"]
    holders = data["Holders"]

    # Increment data by 2
    data["Total Listed"] += 2
    data["Holders"] += 2

    # Save updated data back to data.json
    with open('data.json', 'w') as f:
        json.dump(data, f)

    return {
        'total_listed': total_listed,
        'holders': holders

    }
