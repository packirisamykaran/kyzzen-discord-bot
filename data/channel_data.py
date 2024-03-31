# Store messages in a json file

import json


def store_message(message):
    """
    Store a message in a json file.
    """
    with open("messages.json", "a") as file:
        json.dump(message, file)
        file.write("\n")
