# MONKEY BOT #
#
# Please check todo list sometimes
# There are lots of stuff.
# If you find an issue, open issue, please!
# Thanks!
# 
# MonkeyBot by maxus aka Maxuss aka Void Moment#8152 (c)
#




#region imports
import requests, os, time, asyncio, json, discord, datetime, io, platform
from decouple import config
from random import *
from discord.utils import get
from discord.ext import commands
from data import DATACENTRE as dat
from data import download_auctions
from collections import defaultdict
from re import search
from aiohttp import ClientSession
from data import ExitForLoop
import nest_asyncio as nasync
nasync.apply()
API_KEY = dat.API_KEY
facts = dat.facts
FACT_STR = dat.FACT_STR
multistring = dat.multistring
responses = dat.responses
auctions_path = dat.auctions_path
monke = dat.monke
data = dat.data
voidmoment = dat.voidmoment
monkey_id = dat.monkey_id
pog = dat.pog
REQ_SA = dat.REQ_SA
REQ_SLAYER = dat.REQ_SLAYER
#endregion imports
#region update ah
async def fetch_ah_api():
    while True:
        download_auctions()
        print('Auctions will be updated in 10 minutes!')
        await asyncio.sleep(600)
#endregion update ah
#region prefix

def get_prefix(client, message):
    with open('prefixes.json', 'r') as o:
        prefixes = json.load(o)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, help_command=None)

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as o:
        prefixes = json.load(o)

    prefixes[str(guild.id)] = 'm!'

    with open('prefixes.json', 'w') as o:
        json.dump(prefixes, o, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as o:
        prefixes = json.load(o)
    
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as o:
        json.dump(prefixes, o, indent=4)

@bot.command(name='prefix',help='Changes prefix for current server.')
async def set_prefix(ctx, *, prefix:str):
    if prefix:
        with open('prefixes.json', 'r') as o:
            prefixes = json.load(o)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as o:
            json.dump(prefixes, o, indent=4)
    else:
        resp = 'Invalid command syntax!'
        await ctx.send(embed=embed_error)
#endregion prefix
#region parsing emojis
# Pog no more yansim-styled elif cycle
def parsemoji(cutename: str):
    global fruitmoji
    emoj = {
        'Apple': '🍎',
        'Banana': '🍌',
        'Blueberry': '🍒',
        'Coconut': '🥥',
        'Cucumber': '🥒', 
        'Grapes': '🍇', 
        'Kiwi': '🥝', 
        'Lemon': '🍋',
        'Lime': '🍋',    
        'Mango':'🥭',
        'Papaya':'🥭', 
        'Orange': '🍊',  
        'Peach': '🍑', 
        'Pear': '🍐', 
        'Pineapple': '🍍', 
        'Pomegranate': '🥭',
        'Raspberry': '🍒',
        'Strawberry': '🍓', 
        'Tomato': '🍅',
        'Watermelon': '🍉',
        'Zucchini': '🥬',
    }
    fruitmoji = emoj[cutename]
#endregion parsing emojis
#region stuff


def chooseFact():
    fact = choice(facts)
    return fact

@bot.event
async def on_ready():
    activity = discord.Game(name=dat.RPC_STATUS, type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Fetching api...")
    print("Bot is ready!")
    asyncio.create_task(fetch_ah_api())


#endregion stuff
#region req
@bot.command(name='reqs', help='Checks, if the player has requirements to join guild "Macaques".')
async def reqs(ctx, nickname: str):
    if nickname:
        start_time = time.time()
        lookstr = monke + 'Looking up for player ' + nickname + "'s reqs..." + dat.FACT_STR + chooseFact()
        prev = await ctx.send(lookstr)
        try:
            PLAYER_NAME = nickname
            mojangu = 'https://api.mojang.com/users/profiles/minecraft/'+PLAYER_NAME+'?'
            mojangr = requests.get(mojangu).json()
            UUID = str(mojangr["id"])
            data = requests.get("https://api.hypixel.net/player?key="+ dat.API_KEY + "&name=" + PLAYER_NAME).json()
            data_sb_PATH = data["player"]["stats"]["SkyBlock"]["profiles"]
            profiles = list(data_sb_PATH.keys())
            d = []
            for i in range(0, (len(profiles))):
                sb_data = requests.get("https://api.hypixel.net/skyblock/profile?key="+dat.API_KEY+"&profile="+profiles[i]).json()
                d.append(sb_data["profile"]["members"][UUID]["last_save"])     
            all_save_uuids = dict(zip(profiles, d))
            try:
                last_save = max(all_save_uuids, key=all_save_uuids.get)
            except ValueError:
                raise TypeError
            SB_ID = str(last_save)
            sb_data = requests.get("https://api.hypixel.net/skyblock/profile?key="+API_KEY+"&profile="+SB_ID).json()
            sb_profile = sb_data["profile"]["members"][UUID]
            sb_z_lvl = int(sb_profile["slayer_bosses"]["zombie"]["xp"])
            sb_t_lvl = int(sb_profile["slayer_bosses"]["spider"]["xp"])
            sb_w_lvl = int(sb_profile["slayer_bosses"]["wolf"]["xp"])
            sb_slayer_lvl = int((sb_t_lvl+sb_z_lvl+sb_w_lvl))
            
            sb_mining = data["player"]["achievements"]["skyblock_excavator"]
            sb_farming = data["player"]["achievements"]["skyblock_harvester"]
            sb_combat = data["player"]["achievements"]["skyblock_combat"]
            sb_foraging = data["player"]["achievements"]["skyblock_gatherer"]
            sb_enchanting = data["player"]["achievements"]["skyblock_augmentation"]
            sb_alchemy = data["player"]["achievements"]["skyblock_concoctor"]
            sb_fishing = data["player"]["achievements"]["skyblock_angler"]

            sb_sum = (sb_mining + sb_farming + sb_combat + sb_foraging + sb_enchanting + sb_alchemy + sb_fishing)
            sb_sa = round((sb_sum / 7), 1)

            print(sb_sa)
            print(sb_slayer_lvl)

            if sb_sa >= REQ_SA:
                sa_a = True
                sa_msg = '✅Accepted. Level: ' + str(sb_sa)
            else:
                sa_a = False
                sa_msg = '❌Unaccepted. Level: ' + str(sb_sa)
            if sb_slayer_lvl >= REQ_SLAYER:
                slayer_a = True
                slayer_msg = '✅Accepted. Total XP: ' + str(sb_slayer_lvl)
            else:
                slayer_a = False
                slayer_msg = '❌Unaccepted. Total XP: ' + str(sb_slayer_lvl)

            if sa_a and slayer_a:
                accepted = True
                gtotal = 'User with name ' + nickname + ' acceptable to guild!'
                e_h =  '✅User meets requirements!✅'
            else:
                accepted = False
                gtotal = 'User with name ' + nickname + ' isn\'t acceptable to guild!'
                e_h = '❌User doesn\'t meet requirements!❌'

            sa_h = 'Skill Average:'
            sl_h = 'Slayers:'
            g_h = 'Conclusion'



            time_took = str(round((time.time() - start_time), 3))
            tt = "Time taken on executing command: "
            timetook = time_took + " seconds!"

            return_embed = discord.Embed(title=e_h, description='', color=0xf5ad42)
            return_embed.add_field(name=sa_h, value=sa_msg, inline=False)
            return_embed.add_field(name=sl_h, value=slayer_msg, inline=False)
            return_embed.add_field(name=g_h, value=gtotal, inline=False)
            return_embed.add_field(name=tt, value=timetook, inline=False)

            await prev.edit(content='', embed=return_embed)
            await prev.add_reaction(monkey_id)
        except KeyError:
            resp = 'Looks like there is some API errors! Try turning on/asking to turn on all the API in settings!'
            embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
            await prev.edit(embed=embed_error, content='')
        except TypeError:
            resp = 'Hmm maybe that player doesn\'t exist? Couldn\' get data from API!'
            embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
            await prev.edit(embed=embed_error, content='')
    else: 
        resp = 'Invalid command syntaxis!'
        embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
        await prev.edit(embed=embed_error, content='')
#endregion req
#region sb
@bot.command(name='sb', help='Shows some data about skyblock profile. WIP for now.')
async def sb(ctx, nickname: str):
    if nickname:
        start_time = time.time()
        lookstr = monke + 'Looking up for player ' + nickname + "..." + dat.FACT_STR + chooseFact()
        prev = await ctx.send(lookstr)
        try:
            PLAYER_NAME = nickname
            mojangu = 'https://api.mojang.com/users/profiles/minecraft/'+PLAYER_NAME+'?'
            mojangr = requests.get(mojangu).json()
            UUID = str(mojangr["id"])
            data = requests.get("https://api.hypixel.net/player?key="+API_KEY+"&name=" + PLAYER_NAME).json()
            data_sb_PATH = data["player"]["stats"]["SkyBlock"]["profiles"]
            true_name = data["player"]["knownAliases"][-1]
            profiles = list(data_sb_PATH.keys())
            d = []
            print(profiles)
            for i in range(0, (len(profiles))):
                sb_data = requests.get("https://api.hypixel.net/skyblock/profile?key="+API_KEY+"&profile="+profiles[i]).json()
                d.append(sb_data["profile"]["members"][UUID]["last_save"])
            all_save_uuids = dict(zip(profiles, d))
            print(all_save_uuids)
            try:
                last_save = max(all_save_uuids, key=all_save_uuids.get)
            except ValueError:
                raise TypeError
            print(last_save)
            SB_ID = str(last_save)
            sb_data = requests.get("https://api.hypixel.net/skyblock/profile?key="+API_KEY+"&profile="+SB_ID).json()
            sb_cute_name = data_sb_PATH[SB_ID]["cute_name"]
            sb = sb_data["profile"]["members"][UUID]
            souls = str(sb["fairy_souls_collected"])
            deaths = str(sb["death_count"])
            try:
                bank_money = int(sb_data["profile"]["banking"]["balance"])
                purse_money = round(int(sb["coin_purse"]), 1)
                coins = str(bank_money + purse_money)
            except KeyError:
                coins = '<private>'

            parsemoji(sb_cute_name)

            embed_header = "Found player " + true_name + "'s skyblock profile!"
            embed_pinfo = "Profile Fruit - " + sb_cute_name + " " + fruitmoji
            embed_sinfo = "Fairy Souls collected - " + souls
            embed_dinfo = "Deaths - " + deaths
            embed_cinfo = "Coins in purse - " + coins

            time_took = str(round((time.time() - start_time), 3))
            tt = "Time taken on executing command: "
            timetook = time_took + " seconds!"

            return_embed = discord.Embed(title=embed_header, description='', color=0xf5ad42)
            return_embed.add_field(name='Current Profile', value=embed_pinfo, inline=False)
            return_embed.add_field(name='Souls', value=embed_sinfo, inline=False)
            return_embed.add_field(name='Deaths', value=embed_dinfo, inline=False)
            return_embed.add_field(name='Coins', value=embed_cinfo, inline=False)
            return_embed.add_field(name=tt, value=timetook, inline=False)



            await prev.edit(content='', embed=return_embed)
            await prev.add_reaction(monkey_id)
        except KeyError:
            resp = 'Looks like there is some API errors! Try turning on all the API in settings! ' + nickname
            embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
            await prev.edit(embed=embed_error, content='')
        except TypeError:
            resp = 'Hmm. Maybe player with that nickname doesn\'t exist? Couldn\'t get this player\'s api! Name: "' + nickname + '"'
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
        lookstr = monke + "Looking up for item " + current_item + "..." + FACT_STR + chooseFact()
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
async def sky(ctx, name=None):
    prev = await ctx.send(monke + 'Wait a second... Fun fact: ' + chooseFact())
    if name:
        await asyncio.sleep(0.3)
        skylink = "https://sky.shiiyu.moe/stats/" + name.lower()
        await prev.edit(content=skylink)
    else:
        await prev.edit(content=error_response)
#endregion sky
#region gamble
@bot.command(name='dungeon', help='Run dungeons cus why not lol. Argument 1 is floor, f1-f7. Argument 2 is Boolean(True/False), it showsm whenether you are going to do frag runs. WORKS ONLY ON F6-F7')
async def dungeons(ctx, floor:str, frag=None):
    #region Dungeon Loot
    # DUNGEON LOOT SYNTAX ==> 'type': [name, chance, amount_min, amount_max, cost, cost_from_chest_multiplier] 
    f1 = {
        '0': ['Bonzo\'s Staff', 69, 1, 1, 1500000, 1000000],
        '1': ['Bonzo\'s Mask', 35, 1, 1, 500000, 1000000],
        '2': ['Red Nose', 10, 1, 1, 25000, 10000],
    }
    f2 = {
        '0': ['Scarf Studies', 10, 1, 1, 300000, 10000],
        '1': ['Adaptive Blade', 25, 1, 1, 1000000, 250000],
    }
    f3 = {
        '0': ['Adaptive Boots', 10, 1, 1, 500000, 500000],
        '1': ['Adaptive Helmet', 10, 1, 1, 500000, 500000],
        '2': ['Adaptive Chestplate', 50, 1, 1, 3000000, 1000000],
        '3': ['Adaptive Leggings', 50, 1, 1, 1000000, 1000000],
    }
    f4 = {
        '0': ['Rend I Enchanted Book', 15, 1, 1, 250000, 100000],
        '1': ['[LVL 1] Spirit Pet <Epic>', 25, 1, 1, 500000, 100000],
        '2': ['[LVL 1] Spirit Pet <Legendary>', 25, 1, 1, 1000000, 100000],
        '3': ['Spirit Bone', 23, 1, 2, 4500000, 500000],
        '4': ['Spirit Boots', 23, 1, 1, 1000000, 1000000],
        '5': ['Spirit Wing', 23, 1, 1, 2100000, 2000000],
        '6': ['Spirit Bow', 50, 1, 1, 1000000, 1000000],
        '7': ['Spirit Sword', 50, 1, 1, 1000000, 1000000],
    }
    f5 = {
        '0': ['Overload I Enchanted Book', 5, 1, 1, 50000, 0],
        '1': ['Shadow Assassin Boots', 15, 1, 1, 2000000, 500000],
        '2': ['Shadow Assassin Leggings', 15, 1, 1, 2000000, 500000],
        '3': ['Shadow Assassin Chestplate', 100, 1, 1, 25000000, 2000000],
        '4': ['Shadow Assassin Helmet', 15, 1, 1, 2000000, 500000],
        '5': ['Livid Dagger', 30, 1, 1,  7000000, 3000000],
        '6': ['Warped Stone', 30, 1, 1,  400000, 300000],
        '7': ['Last Breath', 40, 1, 1,  9000000, 3000000],
        '8': ['Shadow Fury', 50, 1, 1,  14000000, 5000000],
    }
    f6 = {
        '0': ['Giant\'s Tooth', 5, 1, 1, 500000, 0],
        '1': ['Ancient Rose', 10, 1, 3, 700000, 200000],
        '2': ['Necromancer Sword', 40, 1, 1,  4000000, 6000000],
        '3': ['Giant\'s Sword', 50, 1, 1,  14000000, 5000000],
        '4': ['Precursor Eye', 80, 1, 1,  20000000, 10000000],
        '5': ['Necromancer Lord Helmet', 20, 1, 1, 2000000, 500000],
        '6': ['Necromancer Lord Chestplate', 100, 1, 1, 15000000, 8000000],
        '7': ['Necromancer Lord Leggings', 20, 1, 1, 2000000, 500000],
        '8': ['Necromancer Lord Boots', 20, 1, 1, 2000000, 500000],
        '9': ['Summonning Ring', 100, 1, 1, 10000000, 8000000],
    }
    f7 = {
        '0': ['Soul Eater I Enchanted Book', 10, 1, 1, 1500000, 1000000],
        '1': ['Precursor Gear', 5, 1, 1, 500000, 300000],
        '2': ['Wither Catalyst', 2, 1, 4, 500000, 100000],
        '3': ['Wither Blood', 5, 1, 1, 1000000, 800000],
        '4': ['Wither Chestplate', 200, 1, 1, 50000000, 15000000],
        '5': ['Wither Helmet', 25, 1, 1, 2000000, 1000000],
        '6': ['Wither Leggings', 25, 1, 1, 10000000, 5000000],
        '7': ['Wither Boots', 25, 1, 1, 2000000, 1000000],
        '8': ['Wither Cloak Sword', 60, 1, 1, 8000000, 5000000],
        '9': ['Wither Scroll', 60, 1, 1, 60000000, 10000000],
        '10': ['Necron\'s Handle', 250, 1, 1, 398000000, 15000000],
    }
    #endregion Dungeon Loot
    #FRAG RUNS TYPE SYNTAXIS==> [name, chance, price]
    #region Frag Runs Loot
    frag6 = {
        '0': ['Livid Fragment', 5, 250000],
        '1': ['Bonzo Fragment', 1, 50000],
        '2': ['Scarf Fragment', 2, 70000],
        '3': ['Ancient Rose', 9, 700000],
    }
    frag7 = {
        '0': ['L.A.S.R. Eye', 5, 800000],
        '1': ['Diamante\'s Handle', 9, 1200000],
        '2': ['Jolly Pink Rock', 2, 20000],
        '3': ['Bigfoot\'s lasso', 2, 40000],
    }
    #endregion Frag Runs Loot
    
    f1_d = 'Floor 1 run'
    f2_d = 'Floor 2 run'
    f3_d = 'Floor 3 run'
    f4_d = 'Floor 4 run'
    f5_d = 'Floor 5 run'
    f6_d = 'Floor 6 run'
    f7_d = 'Floor 7 run'

    fr6_d = 'Frag run on Floor 6'
    fr7_d = 'Frag run on Floor 7'
    waiting = monke + 'Gambling, please wait... ' + chooseFact()
    prev = await ctx.send(waiting)
    start_time = time.time()
    if floor:
        if floor == 'f1':
            flt = f1
            fstr = f1_d
        elif floor == 'f2':
            flt = f2
            fstr = f2_d
        elif floor == 'f3':
            flt = f3
            fstr = f3_d
        elif floor == 'f4':
            flt = f4
            fstr = f4_d
        elif floor == 'f5':
            flt = f5
            fstr = f5_d
        elif floor == 'f6':
            flt = f6
            fstr = f6_d
        elif floor == 'f7':
            flt = f7
            fstr = f7_d
        else:
            resp = 'Invalid Floor!'
            embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
            await prev.edit(embed=embed_error, content='')
        while True:
            if frag:
                if flt == f6:
                    flt = frag6
                    fstr = fr6_d
                    break
                elif flt == f7:
                    flt = frag7
                    fstr = fr7_d
                    break
                else:
                    resp = 'You can\'t frag run this floor!'
                    embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
                    await prev.edit(embed=embed_error, content='')
                    break
            else:
                break
            
        i = 0
        r = 0
        d = {}
        chest_cost = 100000

        for i in flt:
            stri = str(i)
            if flt == frag6 or flt == frag7:
                minim = 1
                maxim = flt[stri][1]
                random_drop = randint(minim, maxim)
                if random_drop == maxim:
                    d["drop{0}".format(i)] = stri
            else:
                minim = 1
                maxim = flt[stri][1]
                random_drop = randint(minim, maxim)
                if random_drop == maxim:
                    d["drop{0}".format(i)] = stri 
    
        i = 0
        money = 0
        list_ids = []
        for i in d.values():
            if i in d.values():
                if flt == frag6 or flt == frag7:
                    money += flt[d["drop{0}".format(i)]][2]
                    item_str = str(flt[d["drop{0}".format(i)]][0])
                    list_ids.append(item_str)
                else:
                    chest_cost += flt[d["drop{0}".format(i)]][5]
                    minim = flt[d["drop{0}".format(i)]][2]
                    maxim = flt[d["drop{0}".format(i)]][3]
                    amount = randint(minim, maxim)
                    item_str = str(flt[d["drop{0}".format(i)]][0])
                    money += ((flt[d["drop{0}".format(i)]][4]*amount) - chest_cost)
                    list_ids.append(item_str)
        
        time_took = str(round((time.time() - start_time), 3))
        tt = "Time taken on executing command: "
        timetook = time_took + " seconds!"
        items_str = ('\n'.join(map(str, list_ids)))


        f1_d = 'Floor 1 run'
        f2_d = 'Floor 2 run'
        f3_d = 'Floor 3 run'
        f4_d = 'Floor 4 run'
        f5_d = 'Floor 5 run'
        f6_d = 'Floor 6 run'
        f7_d = 'Floor 7 run'

        fr6_d = 'Frag run on Floor 6'
        fr7_d = 'Frag run on Floor 7'

        embed_run = 'You did a ' + fstr + '!'
        embed_profit = 'Your total profit is ' + str(money) + ' coins!'
        if list_ids:
            embed_items = 'You got: \n' +  items_str
        else:
            embed_items = 'You got nothing useful this run :('
        
        embed_header = 'Dungeon Run Simulator'

        return_embed = discord.Embed(title=embed_header, description='', color=0xf5ad42)
        return_embed.add_field(name='Run Info', value=embed_run, inline=False)
        return_embed.add_field(name='Profit', value=embed_profit, inline=False)
        return_embed.add_field(name='Items', value=embed_items, inline=False)
        return_embed.add_field(name=tt, value=timetook, inline=False)
        d = defaultdict(dict)
        data_id = str(ctx.message.author.id)


        await prev.edit(embed=return_embed, content='')
        
    else:
        resp = 'Invalid command syntaxis!'
        embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
        await prev.edit(embed=embed_error, content='')
#endregion gamble
#region eat
@bot.command(name='eat', help='Monke eat. Banana/Coconut/Rolety')
async def eat(ctx, *, food):
    gc = [
        'Nah man, not worth it',
        'Cool but meh',
        'Neat, yum yum',
        'Thats some good food',
        'OO AA BEST MONKE FOOD EVER',
        'epic food monke love it oo aa',
        'not bad oo aa',
        'yuck ew',
        'only gold can eat this trash'
    ]
    voidid = '<@381827687775207424>'
    lookstr = 'Monke hungry'
    prev = await ctx.send(lookstr)
    try:
        if not food:
                await prev.edit(content='', embed=embed_error,)
        else:
            if 'banana' in food.lower():
                o = 'banana'
                resp = responses[o]
            elif 'coco' in food.lower():
                o = 'coco'
                resp = responses[o]
            elif 'rolet' in food.lower():
                o = 'rolet'
                resp = responses[o]
            elif 'void' in food.lower():
                o = 'void'
                resp2 = voidid + ' nvm get pinged lol noob.'
                resp = responses[o]
            elif 'cross' in food.lower():
                o = 'cross'
                resp = responses[o]
            elif 'monke' in food.lower():
                o = 'monke'
                resp = responses[o]
            elif 'cum' in food.lower():
                o = 'cum'
                resp = responses[o]
            elif 'masmig' in food.lower():
                o = 'masmig'
                resp = responses[o]
            elif 'starfruit' in food.lower():
                o = 'starfruit'
                resp = responses[o]
            elif 'me' in food.lower():
                o = 'me'
                resp = responses[o]
            elif 'dead cells' in food.lower():
                o = 'dead cells'
                resp = responses[o]
            elif 'chaos' in food.lower():
                o = 'chaos'
                resp = responses[o]
            elif 'weiwei' in food.lower():
                o = 'weiwie'
                resp = responses[o]
            elif 'wurm' in food.lower():
                o = 'wurm'
                resp = responses[o]
            elif 'gold' in food.lower():
                o = 'gold'
                resp = responses[o]
            else:
                resp = choice(gc)
            
            await prev.edit(content=resp)
            if resp2:
                await ctx.send(content=resp2)
    except UnboundLocalError:
        pass
                
#endregion eat
#region respond
@bot.event
  
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if 'good bot' in message.content.lower():
        resp = pog +'Thanks!\nIf you wish to know more about me, visit my GitHub Repository: https://github.com/Maxuss/MonkeyBot/\nThere\'s lots of cool information about me!\nMy creator also has a Patreon page! You can check him out there https://www.patreon.com/maxus_ '
        await message.channel.send(resp)
    elif 'monke' in message.content.lower():
        resp = 'oo oo aa aa monke' + pog + pog + pog
        await message.channel.send(resp)
    elif 'macaque' in message.content.lower():
        resp = 'macaques on top!'
        await message.channel.send(resp)
    elif 'eknom' in message.content.lower(): 
        resp = 'egom yt'
        await message.channel.send(resp)
#endregion respond
#region DEV_CMDS
#region confirm dev
@bot.command(name='confirm_dev', help='Confirms that you are me... Only works with me tho')
async def confirm_dev(ctx):
    dev = obj["dev_mode"]
    if dev != 1:
        verstr = 'I have sent verification input to console!'
        a = await ctx.send(verstr)
        inputa = 'cock'
        if inputa == DEV or inputa == 'DEV':
            await a.edit(content='Access to dev commands granted to this server! Be careful!')
            obj["dev_mode"] = 1
            dev = obj["dev_mode"]
        else:
            await a.edit(content='BLOCKED!')
    else:
        verstr = 'You have already granted dev access to this server! Do m!stop_dev to cancel it!'
        await ctx.send(verstr)
@bot.command(name='stop_dev', help='Stops dev access for current server...')
async def stop_dev(ctx):
    dev = obj["dev_mode"]
    if dev != 1:
        verstr = 'Access denied!'
        await ctx.send(verstr)
    else:
        verstr = 'I have sent verification input to console!'
        a = await ctx.send(verstr)
        inputa = 'cock'
        if inputa == DEV or inputa == 'DEV':
            await a.edit(content='No longer in dev mode!')
            obj["dev_mode"] 
            dev = obj["dev_mode"]
        else:
            await a.edit(content='BLOCKED')
#endregion confirm dev

#endregion DEV_CMDS
#region info
@bot.command(name='info', help='Shows some useful info about bot')
async def info(ctx):
    embed_patrons = 'No one yet :('
    embed_main = 'This is a bot developed by ```Void Moment#8152``` for guild Macaques! \nIt can do some stuff related to Hypixel Skyblock. \nUse m!help for info about commands!'
    embed_ph = 'My Patreon:'
    embed_patre = 'I have a patreon, so if you want to support my work and help me host the bot you can donate! [Link](https://www.patreon.com/maxus_)'
    embed_cp = 'Current Patrons:'
    embed_mh = 'MonkeyBot by VoidMoment aka maxus'
    embed_mih = 'Main info you need to know:'
    
    return_embed = discord.Embed(title=embed_mh, description='', color=0xf5ad42)
    return_embed.add_field(name=embed_mih, value=embed_main, inline=False)
    return_embed.add_field(name=embed_ph, value=embed_patre, inline=False)
    return_embed.add_field(name=embed_cp, value=embed_patrons, inline=False)

    await ctx.send(embed=return_embed)

#endregion info
#region help
@bot.command()
async def help(ctx, page=None):
    hd = 'MB Commands'
    pref = 'Default prefix: m!'
    sy = 'Preset: ```command [required param] <optional param>```\n'
    ment = 'Note: bot updates auction data every **10** minutes. \nDuring that time bot is immune to all the commands.\n'
    a = '```help <page>``` - shows this message.\n'
    b = '```prefix [prefix]``` - sets prefix for current server.\n'
    c = '```reqs [nickname]``` - checks whether the ```nickname``` can join the guild Macaques.\n'
    d = '```sb [nickname]``` - shows a bit of stuff from players account.\n'
    e = '```bz [item]``` - shows all the useful info about item in bazaar.\n'
    f = '```sky [nickname]``` - sends SkyCrypt link of chosen player.\n'
    g = '```dungeon [floor] <?frag>``` - Simulates results of a dungeon run. Also supports frag runs on floor 6/7.\n'
    h = '```eat [item]``` - Makes monkey eat a thing. lol.\n'
    i = '```bin [item]``` - Shows some info about item on BIN. Might not be the lowest price BIN!'
    fullstr = sy + a + b + c + d + e + f + g + h + i
    
    return_embed = discord.Embed(title=hd, description='', color=0xf5ad42)
    return_embed.add_field(name='Prefix', value=pref, inline=False)
    return_embed.add_field(name='Commands', value=fullstr, inline=False)

    await ctx.send(embed=return_embed)
#endregion help
#region ah
data_replaceable = [
    "§0", "§1", "§2", "§3", "§4", "§5", "§6",
    "§7", "§8", "§9", "§c", "§e", "§a", "§b",
    "§d", "§f", "§k", "§l", "§m", "§n", "§o",
    "§r", "RIGHT CLICK", "COMMON", "RARE",
    "LEGENDARY", "EPIC", "MYTHIC", "SPECIAL",
    "VERY SPECIAL", "SUPREME", "Mana Cost",
    "SWORD", "BOW", "ACCESSORY", "ORB", "BOOTS",
    "LEGGINGS", "CHESTPLATE", "HELMET", "DUNGEON"
]
data_replaceable_back = [
    "", "", "", "", "", "", "",
    "", "", "", "", "", "", "",
    "", "", "", "", "", "", "",
    "", "**RIGHT CLICK**", "**COMMON**", "**RARE**",
    "**LEGENDARY**", "**EPIC**", "**MYTHIC**", "**SPECIAL**",
    "**VERY SPECIAL**", "**SUPREME**", "_Mana Cost_",
    "**SWORD**", "**BOW**", "**ACCESSORY**", "**ORB**", "**BOOTS**",
    "**LEGGINGS**", "**CHESTPLATE**", "**HELMET**", "**DUNGEON**"
]
# ah item data: 0name, 1lore, 2rarity, 3starting bid, 4?bought, 5bin auction, 6price, 7title, 8bought ot not
ahs = []
def seek_for_item(ah_dat, item_name):
    try:
        for a in range(len(ah_dat)):
            vals = list(ah_dat[a].values())
            for k in range(len(vals)):
                item = str(vals[k])
                if search(item_name.lower(), item.lower()):
                    found = True
                    tah = ah_dat[a]
                    name = tah["item_name"]
                    lore = tah["item_lore"]
                    trarity = tah["tier"]
                    start_bid = tah["starting_bid"]
                    bought = tah["claimed"]
                    bs = 'BIN Auction'
                    rarity = '**' + trarity + '**'
                    stb = 'Price: ' + str(start_bid) + ' coins'
                    titlee = 'MB Auction'
                    if bought:
                        bus = 'Bought!'
                    else:
                        bus = 'Selling!'
                    ahs.append(name)
                    ahs.append(lore)
                    ahs.append(rarity)
                    ahs.append(start_bid)
                    ahs.append(bus)
                    ahs.append(bs)
                    ahs.append(stb)
                    ahs.append(titlee)
                    raise ExitForLoop('filler filler')
    except ExitForLoop:
        vals.clear()
        pass

@bot.command(name='bin')
async def ah(ctx, *, item_name:str):
    try:
        lookstr = monke + "Looking up for auction " + item_name + ". Note: Auctions update every 10 minutes, so data you get *might* be a bit outdated! " + FACT_STR + chooseFact()
        prev = await ctx.send(lookstr)
        pages = 0
        if 'linux' in str(platform.system()).lower():   
            with open('/home/maxusgame897/MonkeyBot/auction/0.json', 'r', encoding='utf-8', newline='') as pagedata:
                d = json.load(pagedata)
        else:
            with open('.\\auction\\0.json', 'r', encoding='utf-8', newline='') as pagedata:
                d = json.load(pagedata)
        pages = d["totalPages"]
        pglist = list(range(0, pages))
        for i in pglist:
            if 'linux' in str(platform.system()).lower():
                strr = auctions_path + f'/{i}.json'
            else:
                strr = auctions_path + f'\{i}.json'
            with open(strr, 'r', encoding='utf-8', newline='') as td:
                tah_d = json.load(td)
            
            ah = tah_d["auctions"]
            seek_for_item(ah, item_name)
        
        # ah item data: 0name, 1lore, 2rarity, 3start_bid, 4?bought, 5bin auction, 6price, 7title, 
        
        name = str(ahs[0])
        lore = str(ahs[1])
        rarity = str(ahs[2])
        start_bid = ahs[3]
        bus = ahs[4]
        bs = ahs[5]
        stb = ahs[6]
        titlee = ahs[7]

        for i in range(0, (len(data_replaceable) - 1)):
            name = name.replace(data_replaceable[i], data_replaceable_back[i])
            lore = lore.replace(data_replaceable[i], data_replaceable_back[i])
            rarity = rarity.replace(data_replaceable[i], data_replaceable_back[i])


        return_embed = discord.Embed(title=titlee, description='', color=0xf5ad42)
        return_embed.add_field(name=name, value=lore, inline=False)
        return_embed.add_field(name=bus, value=stb, inline=False)

        await prev.edit(content='', embed=return_embed)
        ahs.clear()
    except IndexError:
        resp = 'Looks like this auction doesn\'t exist, or hardly accessible!'
        embed_error = discord.Embed(title='Oops!', description=resp, color=0xa30f0f)
        await prev.edit(embed=embed_error, content='')
#endregion ah
bot.run(dat.TOKEN)
