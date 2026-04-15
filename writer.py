import json

users = {"Axel": "password", "Baxel": "losenord"}
coins = {"Axel": 100, "Baxel": 100}

with open("userData.json", "w") as f:
    json.dump(users, f, indent=4)
with open("userCoins.json", "w") as f:
    json.dump(coins, f, indent=4)