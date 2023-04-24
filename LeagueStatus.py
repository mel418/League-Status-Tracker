import requests
import discord
from discord.ext import tasks, commands
from os import getenv
import dotenv

dotenv.load_dotenv()

API_KEY = getenv('APIkey') #get new API Key
REGION = "NA1"
SUMMONER_NAME = "bawng"
DISCORD_TOKEN = getenv('token') 
#DISCORD_CHANNEL_ID = 1099595483447566349 # Replace with your Discord channel ID
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.command()
async def hello(message):
        await message.channel.send('Hello, meldeeznuts!')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    
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

@tasks.loop(hours=1)
async def check_game_status():
    summoner_id = get_summoner_id()
    game_status = get_game_status(summoner_id)
    USER_ID = await client.fetch_user(535711912160133120)
    if game_status:
        await USER_ID.send(f"{SUMMONER_NAME} is currently in a game!")
    else:
        await USER_ID.send(f"{SUMMONER_NAME} is not currently in a game.")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    check_game_status.start()

client.run(DISCORD_TOKEN)
