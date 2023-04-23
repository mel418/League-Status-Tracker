import requests
import time
from os import getenv
import dotenv
dotenv.load_dotenv()
API_KEY = getenv('APIkey')
REGION = "NA1"
SUMMONER_NAME = "bawng"

def get_summoner_id():
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SUMMONER_NAME}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise Exception(f"Failed to retrieve summoner ID: {response.status_code}")

def get_game_status(summoner_id):
    url = f"https://{REGION}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(f"Failed to retrieve game status: {response.status_code}")


if __name__ == "__main__":
    summoner_id = get_summoner_id()
    while True:
        game_status = get_game_status(summoner_id)
        print(f"Game status: {game_status}")
        time.sleep(600)



