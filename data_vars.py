# MONKEY BOT VARIABLES FOR USE
# 
# These are variables that i moved to different file
# So they wont take much space in bot.py
#
# MonkeyBot by maxus aka Maxuss aka Void Moment#8152 (c)

import requests, json, pretty_errors, discord
from decouple import config

monke = '<a:monke:813481830766346311>'
voidmoment = '<:voidmoment:813482195422806017>'
monkey_id = '<:monkey~1:813495959639556198>'
pog = '<:Monkey_Pog:781768342112436284>'
REQ_SA = 25
REQ_SLAYER = 150000 

with open('data.json', 'r') as mf:
    f = mf.read()

obj = json.loads(f)



ANTISPAM = obj["antispam"]
AS_TIME = obj["antispam_time"]
TOKEN = str(config('DISCORD_TOKEN'))
RPC_STATUS = "m!help"
FACT_STR = "Fun Fact: "
DEV = str(config('DEV'))
API_KEY = str(config('API_KEY'))
GUILD = str(config('GUILD'))
PLAYER_NAME = 'maxus_'
error_response = "Invalid command syntaxis!"
data = requests.get("https://api.hypixel.net/player?key="+API_KEY+"&name=" + PLAYER_NAME).json()
bz_data = requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + API_KEY).json()
auc_data = requests.get("https://api.hypixel.net/skyblock/auctions").json()
data_sb_PATH = data["player"]["stats"]["SkyBlock"]["profiles"]
ah = auc_data["auctions"]
resp = '!'
embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
cutename = ''
facts = [
    'Did you know MonkeyBot is developed on Python?',
    'Did you know MonkeyBot is developed using discord.py library?',
    'Did you know MonkeyBot was developed in less than one week?',
    'Did you know MonkeyBot was inspired by Jerry The Price Checker from SBZ?',
    'Have you tried doing m!info?',
    'Skyblock is endless grind please end me.',
    'Monkeys are actually smarter than people.',
    'This Fact isn\'t fun :(.'
]