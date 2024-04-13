

collection_discord_config = {
    "ServerID": "1218457494226210826",
    "Counter": {
        "CategoryID": "1222187918173540392",
        "Channels": [
            "floorPrice",
            "averagePrice",
            "listed",
            "volumePast24h",
            "salesPast24h",
            "volumePast7d",
            "salesPast7d",
            "totalOwners",
            "SOL",
            "TPS",
        ]
    },
    "CollectionID": "0e8e33630d554702a1619418269808b4",
    "Listeners": {
        "Twitter": "1222544109261291712"
    }
}


# arrange channel


stats_commands = [
    {"name": "floor-price", "stat": "floorPrice", "description": "Get the current floor price",
        "symbol": "SOL", "response": "Floor Price"},
    {"name": "average-price", "stat": "averagePrice",
        "description": "Get the average price", "symbol": "SOL", "response": "Average Price"},
    {"name": "sales-24h", "stat": "salesPast24h",
        "description": "Get sales in the past 24 hours", "symbol": "", "response": "Sales 24H"},
    {"name": "sales-7d", "stat": "salesPast7d",
        "description": "Get sales in the past 7 days", "symbol": "", "response": "Sales 7D"},
    {"name": "sales-30d", "stat": "salesPast30d",
        "description": "Get sales in the past 30 days", "symbol": "", "response": "Sales 30D"},
    {"name": "sales-1h", "stat": "salesPast1h",
        "description": "Get sales in the past hour", "symbol": "", "response": "Sales 1H"},
    {"name": "vol-24h", "stat": "volumePast24h", "description": "Get volume in the past 24 hours",
        "symbol": "SOL", "response": "Volume 24H"},
    {"name": "vol-7d", "stat": "volumePast7d", "description": "Get volume in the past 7 days",
        "symbol": "SOL", "response": "Volume 7D"},
    {"name": "vol-30d", "stat": "volumePast30d", "description": "Get volume in the past 30 days",
        "symbol": "SOL", "response": "Volume 30D"},
    {"name": "vol-1h", "stat": "volumePast1h", "description": "Get volume in the past hour",
        "symbol": "SOL", "response": "Volume 1H"},
    {"name": "total-volume", "stat": "volumeTotal",
        "description": "Get total volume", "symbol": "SOL", "response": "Total Volume"},
    {"name": "usd-vol-24h", "stat": "volumeUsdPast24h",
        "description": "Get USD volume in the past 24 hours", "symbol": "$USD", "response": "USD Volume 24H"},
    {"name": "usd-vol-7d", "stat": "volumeUsdPast7d",
        "description": "Get USD volume in the past 7 days", "symbol": "$USD", "response": "USD Volume 7D"},
    {"name": "usd-vol-30d", "stat": "volumeUsdPast30d",
        "description": "Get USD volume in the past 30 days", "symbol": "$USD", "response": "USD Volume 30D"},
    {"name": "usd-vol-1h", "stat": "volumeUsdPast1h",
        "description": "Get USD volume in the past hour", "symbol": "$USD", "response": "USD Volume 1H"},
    {"name": "vol-7d-change", "stat": "volumePast7dDelta",
        "description": "Get volume change in the past 7 days", "symbol": "%", "response": "Volume 7D Change"},
    {"name": "vol-30d-change", "stat": "volumePast30dDelta",
        "description": "Get volume change in the past 30 days", "symbol": "%", "response": "Volume 30D Change"},
    {"name": "vol-24h-change", "stat": "volumePast24hDelta",
        "description": "Get volume change in the past 24 hours", "symbol": "%", "response": "Volume 24H Change"},
    {"name": "vol-1h-change", "stat": "volumePast1hDelta",
        "description": "Get volume change in the past hour", "symbol": "%", "response": "Volume 1H Change"},
    {"name": "total-owners", "stat": "totalOwners",
        "description": "Get total number of owners", "symbol": "", "response": "Total Owners"},
    {"name": "listed", "stat": "listed", "description": "Get number of listed NFTs",
        "symbol": "", "response": "Listed NFTs"},
    {"name": "floor-7d-change", "stat": "floorPricePast7dDelta",
        "description": "Get floor price change in the past 7 days", "symbol": "%", "response": "Floor Price 7D Change"},
    {"name": "floor-30d-change", "stat": "floorPricePast30dDelta",
        "description": "Get floor price change in the past 30 days", "symbol": "%", "response": "Floor Price 30D Change"},
    {"name": "floor-24h-change", "stat": "floorPricePast24hDelta",
        "description": "Get floor price change in the past 24 hours", "symbol": "%", "response": "Floor Price 24H Change"},
    {"name": "floor-1h-change", "stat": "floorPricePast1hDelta",
        "description": "Get floor price change in the past hour", "symbol": "%", "response": "Floor Price 1H Change"},
    {"name": "floor-change", "stat": "floorPriceDelta", "description": "Get overall floor price change",
        "symbol": "%", "response": "Overall Floor Price Change"},
    {"name": "average-change", "stat": "averagePriceDelta", "description": "Get overall average price change",
        "symbol": "%", "response": "Overall Average Price Change"}
]

stats_group_commands = {
    "stats-sales": {"description": "Get sales statistics", "stats": [
        "salesPast1h",
        "salesPast24h",
        "salesPast7d",
        "salesPast30d"
    ], "response": "Sales Statistics"},
    "stats-volume": {"description": "Get volume statistics", "stats": [
        "volumePast1h",
        "volumePast24h",
        "volumePast7d",
        "volumePast30d",
        "volumeTotal",
        "volumePast1hDelta",
        "volumePast24hDelta",
        "volumePast7dDelta",
        "volumePast30dDelta"
    ], "response": "Volume Statistics"},
    "stats-floor-price": {"description": "Get floor price statistics", "stats": [
        "floorPrice",
        "floorPricePast1hDelta",
        "floorPricePast24hDelta",
        "floorPricePast7dDelta",
        "floorPricePast30dDelta"
    ], "response": "Floor Price Statistics"},
    "stats-usd-volume":  {"description": "Get volume statistics in USD", "stats": [
        "volumeUsdPast1h",
        "volumeUsdPast24h",
        "volumeUsdPast7d",
        "volumeUsdPast30d",
        "volumePast1hDelta",
        "volumePast24hDelta",
        "volumePast7dDelta",
        "volumePast30dDelta"
    ], "response": "Volume Statistics in USD"}

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
    "averagePriceDelta": "Average change",
    "SOL": "SOL",
    "TPS": "TPS"
}


# reverse statistic_channel_names
statistic_channel_names_reverse = {
    v: k for k, v in statistic_channel_names.items()}


def get_collection_discord_config(guild_id):
    return collection_discord_config
