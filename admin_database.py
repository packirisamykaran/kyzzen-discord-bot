

collection_discord_data = {
    "1218457494226210826": {
        "collectionID": "0e8e33630d554702a1619418269808b4",
        "categoryID": "1222187918173540392",
        "board": {
            "category_name": "Mad Lads Stats📊",
            "channels": [
                        "listed",
                        "totalOwners",
                        "averagePrice",
                        "floorPrice",
                        "salesPast24h",
                        "salesPast7d",
                        "volumePast24h",
                        "volumePast7d"]
        },
        "commands": ["hi", "bye"],
        "listeners": {
            "twitter": "1222544109261291712",

        }
    }


}


statistic_channel_names = {
    "floorPrice": "Floor",
    "averagePrice": "Average",
    "salesPast24h": "Sales 24h",
    "salesPast7d": "Sales 7d",
    "salesPast30d": "Sales 30d",
    "salesPast1h": "Sales 1h",
    "volumePast24h": "Vol 24h",
    "volumePast7d": "Vol 7d",
    "volumePast30d": "Vol 30d",
    "volumePast1h": "Vol 1h",
    "volumeTotal": "Total Volume",
    "volumeUsdPast24h": "USD Vol 24h",
    "volumeUsdPast7d": "USD Vol 7d",
    "volumeUsdPast30d": "USD Vol 30d",
    "volumeUsdPast1h": "USD Vol 1h",
    "volumePast7dDelta": "Vol 7d change",
    "volumePast30dDelta": "Vol 30d change",
    "volumePast24hDelta": "Vol 24h change",
    "volumePast1hDelta": "Vol 1h change",
    "totalOwners": "Total Owners",
    "listed": "Listed",
    "floorPricePast7dDelta": "Floor 7d change",
    "floorPricePast30dDelta": "Floor 30d change",
    "floorPricePast24hDelta": "Floor 24h change",
    "floorPricePast1hDelta": "Floor 1h change",
    "floorPriceDelta": "Floor change",
    "averagePriceDelta": "Average change"
}


# reverse statistic_channel_names
statistic_channel_names_reverse = {
    v: k for k, v in statistic_channel_names.items()}


def get_collection_discord_data(guild_id):
    return collection_discord_data.get(str(guild_id), None)
