####### MONKEYBOT
# API KEY IN DOTENV
# imports
import requests
import os
import ndata
import mcuuid
import time
import asyncio
import base64, zlib
import json
from random import *
from discord.utils import get
import discord
from discord.ext import commands

#useful variables
f = open('data.json')
TOKEN = str(os.environ.get('DISCORD_TOKEN'))
API_KEY = str(os.environ.get('API_KEY'))
GUILD = str(os.environ.get('GUILD'))
PLAYER_NAME = 'maxus_'
error_response = "Invalid command syntaxis!"
client = discord.Client()
bot = commands.Bot(command_prefix='m!')
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
    'Have you tried doing m!sb <player_name>?'
]

#region emoji data
monke = '<a:monke:813481830766346311>'
voidmoment = '<:voidmoment:813482195422806017>'
monkey_id = '<:monkey~1:813495959639556198>'
#endregion emoji data
#region parsing emojis
def parsemoji(cutename: str):
    global fruitmoji
    emoj = [
        '🍎',
        '🍌',
        '🍒',
        '🥥',
        '🥒', 
        '🍇', 
        '🥝', 
        '🍋',  
        '🥭', 
        '🍊',  
        '🍑', 
        '🍐', 
        '🍍', 
        '🍓', 
        '🍅',
        '🍉',
        '🥬',
    ]
    #the cycle for parsing:::
    if cutename=='Apple':
        fruitmoji = emoj[0]
    elif cutename=='Banana':
        fruitmoji = emoj[1]
    elif cutename=='Blueberry':
        fruitmoji = emoj[2]
    elif cutename=='Coconut':
        fruitmoji = emoj[3]
    elif cutename=='Cucumber':
        fruitmoji = emoj[4]
    elif cutename=='Grapes':
        fruitmoji = emoj[5]
    elif cutename=='Kiwi':
        fruitmoji = emoj[6]
    elif cutename=='Lemon':
        fruitmoji = emoj[7]
    elif cutename=='Lime':
        fruitmoji = emoj[7]
    elif cutename=='Mango':
        fruitmoji = emoj[8]
    elif cutename=='Orange':
        fruitmoji = emoj[9]
    elif cutename=='Papaya':
        fruitmoji = emoj[8]
    elif cutename=='Peach':
        fruitmoji = emoj[10]
    elif cutename=='Pear':
        fruitmoji = emoj[11]
    elif cutename=='Pineapple':
        fruitmoji = emoj[12]
    elif cutename=='Pomegranate':
        fruitmoji = emoj[8]
    elif cutename=='Raspberry':
        fruitmoji = emoj[2]
    elif cutename=='Strawberry':
        fruitmoji = emoj[13]
    elif cutename=='Tomato':
        fruitmoji = emoj[14]
    elif cutename=='Watermelon':
        fruitmoji = emoj[15]
    elif cutename=='Zucchini':
        fruitmoji = emoj[16]
#endregion parsing emojis

#region sb
@bot.command(name='sb', help='Shows some data about skyblock profile. WIP for now.')
async def sb(ctx, nickname: str):
    if nickname:
        start_time = time.time()
        lookstr = monke + 'Looking up for player ' + nickname + "..."
        prev = await ctx.send(lookstr)
        try:
            PLAYER_NAME = nickname
            data = requests.get("https://api.hypixel.net/player?key="+API_KEY+"&name=" + PLAYER_NAME).json()
            data_sb_PATH = data["player"]["stats"]["SkyBlock"]["profiles"]
            SB_ID = next(iter(data_sb_PATH))
            print(SB_ID)
            mojangu = 'https://api.mojang.com/users/profiles/minecraft/'+PLAYER_NAME+'?'
            mojangr = requests.get(mojangu).json()
            UUID = mojangr["id"]
            print(UUID)
            sb_data = requests.get("https://api.hypixel.net/skyblock/profile?key="+API_KEY+"&profile="+SB_ID).json()
            sb_cute_name = data_sb_PATH[SB_ID]["cute_name"]
            sb = sb_data["profile"]["members"][UUID]
            souls = str(sb["fairy_souls_collected"])
            deaths = str(sb["death_count"])
            bank_money = round(sb["banking"]["balance"], 1)
            purse_money = round(sb["coin_purse"], 1)
            coins = str(bank_money + purse_money)

            parsemoji(sb_cute_name)

            embed_header = "Found player " + PLAYER_NAME + "'s skyblock profile!"
            embed_pinfo = "Profile Fruit - " + sb_cute_name + " " + fruitmoji
            embed_sinfo = "Fairy Souls collected - " + souls
            embed_dinfo = "Deaths - " + deaths
            embed_cinfo = 

            time_took = str(round((time.time() - start_time), 3))
            tt = "Time taken on executing command: "
            timetook = time_took + " seconds!"
            
            return_embed = discord.Embed(title=embed_header, description='', color=0xf5ad42)
            return_embed.add_field(name='Current Profile', value=embed_pinfo, inline=False)
            return_embed.add_field(name='Souls', value=embed_sinfo, inline=False)
            return_embed.add_field(name='Deaths', value=embed_dinfo, inline=False)
            return_embed.add_field(name=tt, value=timetook, inline=False)



            await prev.edit(content='', embed=return_embed)
        except SyntaxError:
            resp = 'Looks like there is no skyblock profiles for player ' + nickname
            embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
            await prev.edit(embed=embed_error, content='')
    else:
        resp = 'Invalid command syntaxis!'
        embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
        await prev.edit(embed=embed_error, content='')

#endregion sb
#region bzp
@bot.command(name='bz', help='Shows data on bazaar item. Recommended only for hardcore flippers.')
async def bz(ctx, *, item: str):
    start_time = time.time()
    if item:
        current_item = item.replace(" ", "_").upper()
        lookstr = monke + "Looking up for item " + current_item + "..."
        prev = await ctx.send(lookstr)
        try:
            bz_item = bz_data["products"][current_item]
            bz_buy = bz_item["quick_status"]["buyPrice"]
            bz_sell = bz_item["quick_status"]["sellPrice"]
            bz_buy_order = str(bz_item["quick_status"]["buyOrders"])
            bz_sell_order = str(bz_item["quick_status"]["sellOrders"])
            bz_buy_volume = str(bz_item["quick_status"]["buyVolume"])
            bz_sell_volume = str(bz_item["quick_status"]["sellVolume"])
            int_bzb = float(bz_buy)
            int_bzs = float(bz_sell)
            r_bzb = round(int_bzb, 1)
            r_bzs = round(int_bzs, 1)
            bz_b = str(r_bzb)
            bz_s = str(r_bzs)
            
            embed_header = 'Bazaar data on "' + current_item + '"'
            
            price_header = 'Item prices:'
            order_header = 'Amount of orders:'
            volume_header = 'Orders volume:'

            price_str = 'Buy: ' + bz_b + ' coins. \nSell: ' + bz_s + ' coins.'
            order_str = 'Buy: ' + bz_buy_order + ' orders. \nSell: ' + bz_sell_order + ' orders.'
            volume_str = 'Buy: ' + bz_buy_volume + ' \nSell: ' + bz_sell_volume

            time_took = str(round((time.time() - start_time), 3))
            tt = 'Time taken on executing command: '
            timetook = time_took + " seconds!"

            return_embed = discord.Embed(title=embed_header, description='', color=0xf5ad42)
            return_embed.add_field(name=price_header, value=price_str, inline=False)
            return_embed.add_field(name=order_header, value=order_str, inline=False)
            return_embed.add_field(name=volume_header, value=volume_str, inline=False)
            return_embed.add_field(name=tt, value=timetook, inline=False)

            await prev.edit(embed=return_embed, content='')
            await prev.add_reaction(monkey_id)
        except KeyError:
            errorstr = "An error occurred! Looks like item name was written wrong!"
            embed_e = discord.Embed(title=('Oops! Item '+current_item+' doesn\'t exist!'), description=errorstr, color=0xa30f0f)
            await prev.edit(content='', embed=embed_e)
    else: 
        await prev.edit(content='', embed=embed_error,)
#endregion bzp
#region sky
@bot.command(name='sky', help='Show sky.shiiyu.moe profile for player! Syntaxis: m!sky (nickname)')
async def sky(ctx, *, name: str):
    if name:
        await asyncio.sleep(0.3)
        skylink = "https://sky.shiiyu.moe/stats/" + name 
        await ctx.send(skylink)
    else:
        await prev.edit(content=error_response)
#endregion sky
#region gamble !!!! STILL IN WIP !!!!
@bot.command(name='sb_gamble', help='Gamble skyblock cus why not lol. Argument 1: "dungeon floor e.g: f5", "dragon", "slayer type. e.g: rev", "frag run: e.g: \'frag6\'. Available floor for frag running: frag6, frag7')
async def gamble(ctx, arg):
    # LOOT FORMAT ==> "Loot name": [drop_chance(one in how much), drop_amount_min, drop_amount_max, cost]
    #region Dragon loot  
    dragon_loot = { 
        '{LVL 1} Ender Dragon <Epic>': [100, 1, 1, 84500000],
        'Dragon Claw': [10, 1, 1, 1200000],
        'Dragon Scale': [10, 1, 1, 1200000],
        'Aspect Of The Dragons': [8, 1, 1, 2400000],
        'Dragon Fragments': [1, 5, 25, 10000],
        'Dragon Helmet': [4, 1, 1, 1000000],
        'Dragon Chestplate': [4, 1, 1, 2500000],
        'Dragon Leggings': [4, 1, 1, 2000000],
        'Dragon Boots': [4, 1, 1, 1000000],
    }
    sup_only = {
        '{LVL 1} Ender Dragon <Legendary>': [150, 1, 1, 400000000],
        'Dragon Horn': [10, 1, 1, 8000000]
    }
    # TYPE FORMAT ==> "Type name": [loot_cost_multiplier]
    dragon_types = { 
        'Old': [0.5],
        'Protector': [0.4],
        'Young': [1.2],
        'Strong': [1.5],
        'Unstable': [1],
        'Superior': [5],
        'Wise': [1.6],
    }
    #endregion Dragon Loot

    #region Slayer loot
    rev = {
        'Revenant Flesh': [1, 46, 64, 1],
        'Foul Flesh': [5, 2, 4, 20000],
        'Pestilence Rune I': [5, 1, 1, 2000],
        'Undead Catalyst': [10, 1, 1, 10000],
        'Smite VI Enchanted Book': [10, 1, 1, 10000],
        'Beheaded Horror': [100, 1, 1, 50000],
        'Revenant Catalyst': [10, 1, 1, 20000],
        'Snake Rune I': [120, 1, 1, 100000],
        'Scythe Blade': [255, 1, 1, 5000000]
    }
    tara = {
        'Tarantula Web': [1, 46, 64, 10],
        'Toxic Arrow Poison': [5, 46, 64, 5000],
        'Bite Rune I': [5, 1, 1, 25000],
        'Spider Catalyst': [10, 1, 1, 5000],
        'Bane of Arthropods VI Enchanted Book': [100, 1, 1, 10000],
        'Fly Swatter': [],
        'Tarantula Talisman': [],
        'Digested Mosquito': [],
    }
    sven = {
        'Wolf Teeth': [],
        'Hamster Wheel': [],
        'Spirit Rune I': [],
        'Critical VI Enchanted Book': [],
        'Red Claw Egg': [],
        'Couture Rune I': [],
        'Overflux Capacitor': [],
        'Grizzly Bait': [],
    }
    #endregion Slayer loot

    #region Dungeon Loot

    everywhere = {
        'Trash Books': [],
        'Necromancer\'s Brooch': [],
        'Combo I Enchanted Book': [],
        'Ultimate Wise I Enchanted Book': [],
        'Lethality VI Enchanted Book': [],
        'Hot Potato Book': [],
        'Fuming Potato Book': [],
        'Recombobulator 3000': [],
        'Wisdom I Enchanted Book': [],
    }
    f1 = {
        'Bonzo\'s Staff': [],
        'Bonzo\'s Mask': [],
        'Red Nose': [],
    }
    f2 = {
        'Scarf Studies': [],
        'Adaptive Blade': [],
    }
    f3 = {
        'Adaptive Boots': [],
        'Adaptive Helmet': [],
        'Adaptive Chestplate': [],
        'Adaptive Leggings': [],
    }
    f4 = {
        'Rend I Enchanted Book': [],
        '{LVL 1} Spirit Pet <Epic>': [],
        '{LVL 1} Spirit Pet <Legendary>': [],
        'Spirit Bone': [],
        'Spirit Boots': [],
        'Spirit Wing': [],
        'Spirit Bow': [],
        'Spirit Sword': [],
    }
    f5 = {
        'Overload I Enchanted Book': [],
        'Shadow Assassin Boots': [],
        'Shadow Assassin Leggings': [],
        'Shadow Assassin Chestplate': [],
        'Shadow Assassin Helmet': [],
        'Livid Dagger': [],
        'Warped Stone': [],
        'Last Breath': [],
        'Shadow Fury': [],
    }
    f6 = {
        'Giant\'s Tooth': [],
        'Ancient Rose': [],
        'Necromancer Sword': [],
        'Giant\'s Sword': [],
        'Precursor Eye': [],
        'Necromancer Lord Helmet': [],
        'Necromancer Lord Chestplate': [],
        'Necromancer Lord Leggings': [],
        'Necromancer Lord Boots': [],
        'Summonning Ring': [],
    }
    f7 = {
        'Soul Eater I Enchanted Book': [],
        'Precursor Gear': [],
        'Wither Catalyst': [],
        'Wither Blood': [],
        'Wither Chestplate': [],
        'Wither Helmet': [],
        'Wither Leggings': [],
        'Wither Boots': [],
        'Wither Cloak Sword': [],
        'Wither Scroll': []
    }
    #endregion Dungeon Loot

    #region Frag Runs Loot
    frag6 = {
        'Livid Fragment': [],
        'Bonzo Fragment': [],
        'Scarf Fragment': [],
    }
    frag7 = {
        'L.A.S.R. Eye': [],
        'Diamante\'s Handle': [],
        'Jolly Pink Rock': [],
        'Bigfoot\'s lasso': []
    }
    #endregion Frag Runs Loot
    await ctx.send("This command is WIP!")
    # The CODE
    
    #parsing argument
    grinding = arg
    # Moved argument to grinding so
    # we can use it later more easily
    # EDIT01: Fixed insane if-elif structure
#endregion gamble
#region client
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    if 'monke' in message.content:
        resp = 'oo oo aa aa monke'
        await message.channel.send(resp)
    else:
        return
#endregion client
bot.run(TOKEN)
client.run(TOKEN)
