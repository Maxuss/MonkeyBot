# MONKEY BOT VARIABLES FOR USE
# 
# These are variables that i moved to different file
# So they wont take much space in bot.py
#
# MonkeyBot by maxus aka Maxuss aka Void Moment#8152 (c)

import requests, json, pretty_errors, discord, asyncio, aiohttp, os, time, os.path
from decouple import config
from threading import Thread
import nest_asyncio as nasync
nasync.apply()

class DATACENTRE:
    # all the vars needed for now
    monke = '<a:monke:813481830766346311>'
    voidmoment = '<:voidmoment:813482195422806017>'
    monkey_id = '<:monkey~1:813495959639556198>'
    pog = '<:Monkey_Pog:781768342112436284>'
    REQ_SA = 25
    REQ_SLAYER = 150000 

    with open('data.json', 'r') as mf:
        f = mf.read()

    obj = json.loads(f)

    val_channels = [
        "814858417675960330",
        "816761364507787295",
        "702040764095529040",
        "702042560557744148",
        "741750311823081483",
        "702044494954233896",
    ]

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
    data_sb_PATH = data["player"]["stats"]["SkyBlock"]["profiles"]
    resp = '!'
    embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
    cutename = ''
    facts = [
        'Did you know MonkeyBot is developed on Python?',
        'Did you know MonkeyBot is developed using discord.py library?',
        'Did you know MonkeyBot 1.0 was developed in jsut around few weeks?',
        'Did you know MonkeyBot was inspired by Jerry The Price Checker from SBZ?',
        'Have you tried doing m!info?',
        'Skyblock is endless grind please end me.',
        'Monkeys are actually smarter than people(False).',
        'This Fact isn\'t fun :(.',
        'Monkeys use grooming t strengthen their relationship.',
        'Some monkeys are close to extinction :(.',
        'Monkeys got tails quite recently.',
        "Pygmy marmosets are the world's smallest monkeys.",
        'Mandrills are the world largest monkeys',
        'Capuchins monkeys can use tools!',
        'Howler monkeys are the loudest monkeys(OO AA).',
        'Japanese monkeys enjoy relaxing in hot bath.',
        'There are only 1 monkey species in Europe.',
        'Server with this bot is hosted in Netherlands!',
        'Asyncronous programming is so hard, I spent over 2 days making AH command with it!',
        'Hello World!',
        'Goodbye World!',
        'Asyncio is overcomplicated.',
        'This statement is False',
        'MonkeyBot updates it\'s AH database every 10 minutes!',
        'This bot uses more imports, than AOTG\'s braincells!',
        ':Fact Fun ...',
        ' ',
        'Now with bugs!',
        'If you ever find bugs, please open an issue in my github project! You can find link in m!info!',
        'If you want to request a new feature, open an issue in my github project! You can find link in m!info!',
        'This is fact 33!',
        'There are total of 36 facts at the moment!',
        'You can support me by donating to my patreon! You can find link in m!info!',
        'I hate school.'
    ]

    multistring = "banana.green coconut.rolety.void moment.crossmane.monkey.cum.masmig.starfruit.me.dead cells.chaos.weiwei123.wispish wurm.aspect of the gold"
    responses = {
        "banana": 'yummy yummy monke love bananas ',
        "coco": 'monke love green coconuts yummy yummy ',
        "rolet": 'peepeepoopoo :P',
        "void": 'Ping bad',
        "cross": 'Penguz yum yum',
        "monke": 'no',
        "cum": 'tf is wrong with you',
        "masmig": 'monkey not eat noobs oo aa',
        "starfruit": 'that will make good wine ngl',
        "me": 'uh oh stinky',
        "dead cells": '5bc e z',
        "chaos": 'flip bad bad',
        "weiwei": 'wurm',
        "wurm": 'god',
        "gold": 'ew'
    }
    auctions_path = str(config('PATH_TO_AH'))

# DOWNLOADS WHOLE AH API
# THX FOR RANDOM USER ON HYPIXEL FORUMS FOR THIS
# <3
import requests, json, pretty_errors, discord, asyncio, aiohttp, os, time
import data


async def fetch_one_url(session, url, save_path=None):
    # print_timestamp()
    async with session.get(url) as response:
        time.sleep(0.1)
        response_text = await response.text()
        if save_path is not None:
            with open(save_path, "wb") as text_file:
                text_file.write(response_text.encode("UTF-8"))
        return url, response_text

# dowloads everything from urls, then returns with response
def download_urls(urls: list, save_as={}):
    loop = asyncio.get_event_loop()
    htmls = loop.run_until_complete(download_urls_helper(urls, save_as))
    return htmls


async def download_urls_helper(urls: list, save_as: dict):
    # print("Downloading:")
    # print(urls)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            if url in save_as:
                save_path = save_as[url]
            else:
                save_path = None
            tasks.append(fetch_one_url(session, url, save_path))
        htmls = await asyncio.gather(*tasks)

        # print("Finished downloading")
        # print_timestamp()
        return htmls

# end DOWNLOAD URLS

def get_number_of_pages():
    with open('auction/0.json', 'rb') as f:
        ah_dict = json.load(f)
        if ah_dict['success']:
            number_of_pages = ah_dict['totalPages']
            return number_of_pages
        else:
            print("number_of_pages error")



def download_auctions():
    global auctions_json_list
    global auction_list
    print("Updating all auctions")
    # print("Deleting old auction files")
    for filename in os.listdir('auction'):
        os.remove('auction/' + filename)

    # print("Downloading page 0")
    r = requests.get('https://api.hypixel.net/skyblock/auctions?key=' + DATACENTRE.API_KEY + '&page=0')
    with open(r'auction/0.json', 'wb') as f:
        f.write(r.content)
    number_of_pages = get_number_of_pages()
    print("Downloading", number_of_pages, "pages")

    if number_of_pages is None:
        raise Warning('Problems with AH API! Downloading two empty pages!')
        print('dl 2 pg')
        number_of_pages = 2

    urls = []
    save_as = {}
    for page_number in range(1, number_of_pages):
        url = 'https://api.hypixel.net/skyblock/auctions?key=' + DATACENTRE.API_KEY + '&page=' + str(page_number)
        urls.append(url)
        save_as[url] = r'auction/' + str(page_number) + '.json'

    download_urls(urls, save_as)
    print("auctions updated")


### EXCEPTIONS ###
# still indev ;-;

class Error(Exception):
    pass

class ExitForLoop(Error):
    pass
