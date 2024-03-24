

collection_discord_data = {
    "1218457494226210826": {
        "collectionID": "0e8e33630d554702a1619418269808b4",
        "board": {
            "category_name": "Mad Lads Stats📊",
            "channels": ["averagePrice", "floorPrice"]
        },
        "commands": ["hi", "bye"]
    }


}


statistic_channel_names = {
    "floorPrice": "Floor Price",
    "averagePrice": "Average Price"
}


# reverse statistic_channel_names
statistic_channel_names_reverse = {
    v: k for k, v in statistic_channel_names.items()}


def get_collection_discord_data(guild_id):
    return collection_discord_data.get(str(guild_id), None)
