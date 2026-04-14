import json

users = {"Axel": "password", "Baxel": "losenord"}

with open("userData.json", "w") as f:
    json.dump(users, f, indent=4)