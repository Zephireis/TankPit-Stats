import random
import discord
import asyncio
import aiohttp
import requests
import json
import html5lib
import os
import asyncio
import threading
import sqlite3
import mysql.connector

from datetime import datetime




from discord import Game
from bs4 import BeautifulSoup
from discord.ext.commands import Bot



TOKEN = "" #need to use environment variables
BOT_PREFIX = ".","https://tank"


client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')





#================FUN COMMANADS================================================================================

@client.command(name='8ball', pass_context=True)
async def eight_ball(ctx):
    possible_responses = [
    'that is a resounding no',
    'It is not looking likely',
    'Too hard to tell',
    'definitely',
    'idc',
    'probably',
    'sure',
    'no',
    'maybe',
    'its quite possible'

    ]
    await ctx.send(random.choice(possible_responses))


@client.command(pass_context=True)
async def help(ctx):
       embed = discord.Embed(title=' ', description='Prefix: .', color=0x4ec115)
       embed.add_field(name="TankPit Commands", value="``.tp`` ``.prf`` ``.report`` ``.id`` ``.tourny`` ``.results`` ``.bb`` ``.pst`` ``.season``", inline=True)
       embed.add_field(name="General Commands", value="``help``,``info``,``8ball``,``serverinfo``", inline=False)
       embed.set_author(name="TankPit Command List", icon_url='https://tankpit.com/images/icons/red_orb.png')
       embed.set_thumbnail(url='https://tankpit.com/images/icons/green.png')
       embed.set_image(url='https://tankpit.com/images/hero.png',)
       embed.set_footer(text='To get tank stats set your tank stats to public')

       await ctx.send(ctx.message.author, embed=embed)



@client.command(pass_context=True)
async def serverinfo(ctx):
       embed = discord.Embed(title="Tankpit bot", description="Grabs api stats on player profiles", color=0x00ff00)
       embed.add_field(name="Author", value="Zephireis")
       embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
       embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
       embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
       embed.add_field(name="Members", value=len(ctx.message.server.members))
       embed.add_field(name="Server count", value=f"{len(client.servers)}")
       embed.add_field(name="Invite", value="[]()")
       embed.set_thumbnail(url=ctx.message.server.icon_url)
       await client.send(embed=embed)

#================TANK STATS COMMANDS================================================================================

def award_string(seq: list) -> str:
    emoji_set = [
        ['','<:S_Star_New:476303220570849301>','<:D_Star_New:476303233640431617>','<:T_Star_new:476303253794062348>'],
        ['','<:tankb2:476998057595240469>','<:tanks2:476997284878483466>','<:tankg2:476996100377804802>'],
        ['','<:C_Honor_New:476303395288776705>','<:B_Honor_New:476303426985132053>','<:H_Honor_New:476303438142111746>'],
        ['','<:shiner:874792229405863997>','<:b_battered:874792269230792725>','<:r_rusty:874792283181023343> '],
        ['','', '','<:DoT_New:476303764580597761>'],
        ['', '<:B_Cup_New:476303841562853377>','<:S_Cup_New:476303857924833290>','<:G_Cup_New:476303868486221824>'],
        ['','<:PH_New:476303889143037952>','<:PH_New:476303889143037952>','<:PH_New:476303889143037952>'],
        ['','<:WC_New:476303897737297931>','',''],
        ['','<:LB_New:476303919870640130>','',''],
    ]
    if len(seq) != 9:
        raise Exception('Invalid Length')
    awards = [emoji_set[i][award] for i,award in enumerate(seq)]
    return ''.join(awards)
@client.command(pass_context=True)
async def tp(ctx, * tank):
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/find_tank?name={tank}')
        await asyncio.sleep(2)
        COLORS = {
        'red': '<:r_:524455235188424718>',
        'blue': '<:b_:480148438487531520>',
        'purple': '<:p_:524458234803650580>',
        'orange': '<:o_:524458234694860800>',
        }
        embedColor = {
        'red': 0xff0000,
        'blue': 0x5c67ff,
        'purple': 0xbd23d1,
        'orange': 0xe68033,
        }
        resp_json = await response.json()
        ids = resp_json[0]['tank_id']
        NAME = resp_json[0]['name']
        awards = award_string(resp_json[0]['awards'])
    async with aiohttp.ClientSession()as sess:
        respons = await sess.get(f'https://tankpit.com/api/tank?tank_id={ids}')
        resp = await respons.json()
        team = resp['main_color'] #tank color
        embed=discord.Embed(title=f"{COLORS[team]} {NAME}#{ids}", url=f"https://tankpit.com/tank_profile/?tank_id={ids}", description=f"{awards}", color=embedColor[team])
        embed.set_footer(text='use command .id'f' {ids}'' for indepth tank stats')
        try:
            time = resp["map_data"]["World"]["time_played"]
        except:
            embed.set_footer(text="Players 'World' Stats 'time played' not set to public")
        try:
            ranks = resp["map_data"]["World"]["rank"]
        except:
            embed.set_footer(text="Players 'World' Stats 'rank' not set to public")
        try:
            kills = resp["map_data"]["World"]["destroyed_enemies"]
            deac = resp ["map_data"]["World"]["deactivated"]
            ratio = kills / deac
            kd =(round(ratio, 2))
        except:
            embed.set_footer(text="Players 'World' Stats 'kills' not set to public")
            kd = "\u200b"
        try:
            deac = resp ["map_data"]["World"]["deactivated"]
        except:
            embed.set_footer(text="Players 'World' Stats 'deactivated' not set to public")
        lastplayed =  resp.get("last_played", "\u200b")
        favm = resp.get("favorite_map", "\u200b")
        bftank= resp.get("bf_tank_name", "\u200b")
        pong = resp.get("ping", "\u200b")
        location = resp.get("country", "\u200b")
        Bio = resp.get("profile", "\u200b")
        tptank = resp.get("name", "\u200b")
        space ="\u200b"
        try:
            cups = resp['user_tournament_victories'] ['bronze']
        except KeyError:
            a = "<:B_Cup_New:476303841562853377>x0"
        try:
            cups1 = resp['user_tournament_victories'] ['silver']
        except:
            b= "<:S_Cup_New:476303857924833290>x0"
        try:
            cups2 = resp['user_tournament_victories'] ['gold']
        except:
            c = "<:G_Cup_New:476303868486221824>x0"

        try:
            embed.add_field(name="Time Played", value=f'{time}{space}', inline=True)
        except:
            embed.add_field(name="Time Played", value="\u200b", inline=True)
        try:
            embed.add_field(name="Rank", value=f'{ranks}{space}', inline=True)
        except:
            embed.add_field(name="Rank", value=f'\u200b', inline=True)
        try:
            embed.add_field(name="Kills", value=f'{kills}{space}', inline=True)
        except:
            embed.add_field(name="Kills", value='\u200b', inline=True)
        try:
            embed.add_field(name="Deaths", value=f'{deac}{space}', inline=True)
        except:
            embed.add_field(name="Deaths", value='\u200b', inline=True)
        try:
            total = cups + cups1 + cups2
            embed.add_field(name=f"Total Cups#{total}", value=f'<:B_Cup_New:476303841562853377>x{cups}<:S_Cup_New:476303857924833290>x{cups1}<:G_Cup_New:476303868486221824>x{cups2}{space}', inline=True)
        except:
            embed.add_field(name=f"Total Cups", value=f"{a}{b}{c}", inline=True)
        embed.add_field(name="Last played", value=resp.get("last_played", "\u200b"), inline=True)
        embed.add_field(name="K/D Ratio", value=kd, inline=True)
        await ctx.send(embed=embed)



@client.command(pass_context=True)
async def top5(ctx, *tank):
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/find_tank?name={tank}')
        resp_json = await response.json()
        ids = resp_json[0]['tank_id']
        NAME0 = resp_json[0]['name']
        awards0 = award_string(resp_json[0]['awards'])
        space ="\u200b"
        embed = discord.Embed(title=f"Top 5 {NAME0}", description=f"{awards0}", color=0x00ff00)
     
        
        page= requests.get(f"https://tankpit.com/tank_profile/?tank_id={ids}")
        soup = BeautifulSoup(page.content, 'html.parser')
        tanklist = []
        for tanks in soup.find_all('b'):
          tanklist.append(tanks.text)
        if len(tanklist) <= 5:
          await ctx.send("Pleas enable your top 5 tanks inside your profile settings")
          print(tanklist)
        else:
          async with aiohttp.ClientSession()as sessionOtherTanks1:
            response1 = await sessionOtherTanks1.get(f'https://tankpit.com/api/find_tank?name={tanklist[1]}')
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=False)
            await asyncio.sleep(1)

          async with aiohttp.ClientSession()as sessionOtherTanks1:
            response1 = await sessionOtherTanks1.get(f'https://tankpit.com/api/find_tank?name={tanklist[2]}')
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=False)
            await asyncio.sleep(1)
            
          async with aiohttp.ClientSession()as sessionOtherTanks1:
            response1 = await sessionOtherTanks1.get(f'https://tankpit.com/api/find_tank?name={tanklist[3]}')
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=False)
            await asyncio.sleep(1)
            
          async with aiohttp.ClientSession()as sessionOtherTanks1:
            response1 = await sessionOtherTanks1.get(f'https://tankpit.com/api/find_tank?name={tanklist[4]}')
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=False)
            await asyncio.sleep(1)

          async with aiohttp.ClientSession()as sessionOtherTanks1:
            response1 = await sessionOtherTanks1.get(f'https://tankpit.com/api/find_tank?name={tanklist[5]}')
            resp_json1 = await response1.json()
            NAME1 = resp_json1[0]['name']
            awards1 = award_string(resp_json1[0]['awards'])
            embed.add_field(name=f'{NAME1}\n{awards1}', value=f"{space}", inline=False)
            await asyncio.sleep(1)
            await ctx.send(embed=embed)




@client.command(pass_context=True)#updated 08/20/2021
async def season(ctx, year): 
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/leaderboards/'+year)
        resp = await response.json()
        space ="\u200b"
        COLORS = {
        'red': '<:r_:524455235188424718>',
        'blue': '<:b_:480148438487531520>',
        'purple': '<:p_:524458234803650580>',
        'orange': '<:o_:524458234694860800>',
        }
        rankdict = {
        'general': '<:gstar3:874788543287930890>',
        'colonel': '',
        'major' : '',
        }
        leaderboardresults= []
        gameResults = resp['results']
        for players in gameResults:
          leaderboardresults.append(players)
        embed_message = ""
        for i in range(25): #list is 25 in length
            tank = gameResults[i]['name']
            place = gameResults[i]['placing']
            color = gameResults[i]['color']
            rank = gameResults[i]['rank']
            faction = COLORS[color]
            ranks = rankdict[rank]
            embed_message += str(faction) + str(ranks) + " " + str(place) + ":" + " " + str(tank) + "\n"
        embed = discord.Embed(title=f"Top 25 Season {year}", description=embed_message,  color =0xdd3d20)
        # embed.add_field(name="", value=embed_message, inline=False)
        await ctx.send(embed=embed)
        
@client.command(pass_context=True)#updated 08/20/2021
async def tourny(ctx, id):
    async with aiohttp.ClientSession()as session:
        response = await session.get('https://tankpit.com/api/tournament_results?tournament_id=' + id)
        resp = await response.json()
        date = resp["start_time_utc"]
        space ="\u200b"
        COLORS = {
        'red': '<:r_:524455235188424718>',
        'blue': '<:b_:480148438487531520>',
        'purple': '<:p_:524458234803650580>',
        'orange': '<:o_:524458234694860800>',
        }
        rankdict = {
        'general': '<:gstar3:874788543287930890>',
        'colonel': '<:d_col:874790296855134218>',
        'major' : '<:S_Star_New:476303220570849301>',
        'captain' : '<:goldcpt:746222968484397076>',
        'lieutenant' : '<:lieu:874866088293310514>',
        'sergeant' : '<:sgt:874866049533767720>',
        'corporal' : '<:corp:874866014356111420>',
        'private' : '<:pvt:874865999009185792>',
        'recruit ' : '<:rec:874865943560482816>',
        }
        leaderboardresults= []
        gameResults = resp['results']
        for players in gameResults:

          leaderboardresults.append(players)
        embed_message = ""
        for i in range(15): #list is 25 in length
            tank = gameResults[i]['name']
            place = gameResults[i]['placing']
            color = gameResults[i]['color']
            rank = gameResults[i]['rank']
            faction = COLORS[color]
            ranks = rankdict[rank]
            embed_message += str(ranks) + str(faction) + " " + str(place) + ":" + " " + str(tank) + "\n"
        embed = discord.Embed(title=f"Tournament results {date}", description=embed_message,  color =0xdd3d20)
        # embed.add_field(name="", value
        await ctx.send(embed=embed)



@client.command(pass_context=True)#updated 08/20/2021
async def acti(ctx):
    embed = discord.Embed(title="", description="",  color =0xff0000)
    page= requests.get("https://tankpit.com")
    soup = BeautifulSoup(page.content, 'html.parser')

    data = soup.find(id="hero-activity")
    activity = data("p")[0].get_text()
    activity2 = data("p")[1].get_text()
    maps = data("p")[3].get_text()
    WORLD = { #dictonary of map name and img links
    'Rocks and Swamp': 'https://tankpit.com/images/maps/field01.gif',
    'The Pit': 'https://tankpit.com/images/maps/field18.gif',
    'The Nile': 'https://tankpit.com/images/maps/field13.gif',
    'Crazy Maze': 'https://tankpit.com/images/maps/field02.gif',
    'Appaloosa land': 'https://tankpit.com/images/maps/field03.gif',
    'Castles': 'https://tankpit.com/images/maps/field04.gif',
    'Desert': 'https://tankpit.com/images/maps/field05.gif',
    'Iceland': 'https://tankpit.com/images/maps/field06.gif',
    'Deep Six': 'https://tankpit.com/images/maps/field07.gif',
    'Levels': 'https://tankpit.com/images/maps/field08.gif',
    'Metropolis': 'https://tankpit.com/images/maps/field09.gif',
    'Elements': 'https://tankpit.com/images/maps/field21.gif',
    'Orbital': 'https://tankpit.com/images/maps/field23.gif',
    'Trump': 'https://tankpit.com/images/maps/field24.gif',
    'Intricacy':'https://tankpit.com/images/maps/field25.gif',
    'Confluence':'https://tankpit.com/images/maps/field26.gif',
    'Eruption':'https://tankpit.com/images/maps/field27.gif',
    'Muspelheim':'https://tankpit.com/images/maps/field28.gif',
    'Glacier':'https://tankpit.com/images/maps/field29.gif',
    'Tailing Ponds':'https://tankpit.com/images/maps/field30.gif',
    'Ruins':'https://tankpit.com/images/maps/field31.gif',
    'Soul Swamp':'https://tankpit.com/images/maps/field32.gif',
    'Oasis':'https://tankpitmaps.neocities.org/mapimages/field33.gif',
    'Namek':'https://tankpit.com/images/maps/field34.gif',
    'Gauntlet':'https://tankpit.com/images/maps/field35.gif',
    'Psycho Maze':'https://tankpit.com/images/maps/field36.gif',
    'Treasure Island':'https://tankpit.com/images/maps/field37.gif',
    'Dragon':'https://tankpit.com/images/maps/field38.gif',
    'Dust':'https://tankpit.com/images/maps/field39.gif',
    'Amazon':'https://tankpit.com/images/maps/field40.gif',
    'Lost World':'https://tankpit.com/images/maps/field41.gif',
    'Meltdown':'https://tankpit.com/images/maps/field42.gif',
    'Monoliths':'https://tankpit.com/images/maps/field43.gif',
    'Rura Penthe':'https://tankpit.com/images/maps/field44.gif',
    }
    # searchKey = f"{maps}"
    # if searchKey in WORLD:
    #     print(WORLD[maps])
    embed = discord.Embed(title="TankPit", description="Current players in game",  color =0xdd3d20)
    embed.set_thumbnail(url=f'{WORLD[maps]}')
    embed.add_field(name="In Game", value=activity, inline=False)
    embed.add_field(name="Lobby", value=activity2, inline=False)
    embed.add_field(name="Map", value=maps , inline=True)
    await ctx.send(embed=embed)
   
@client.command(pass_context=True) #DONT FORGET TO CLOSE DATABASE CONNECTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def regtank(ctx, *args):
    mydb = mysql.connector.connect(host="",
    user="",
    passwd="",
    database="")
    teamName = ' '.join(args) #if there is a space in the string it will create a space in the string
    authorid = ctx.message.author.id #discord user id
    authorname = ctx.message.author.name
    print(teamName)

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT discord, tankid FROM players")
    myresult = mycursor.fetchall()
    for x in myresult:
        if authorname in x:
            await ctx.send("Hey you already registered your main tank!\nuse command ``.mytank``")
            return
    await ctx.author.send(f"<@{authorid}> enter your tank ID\n``hint:`` you can find your tank ID #number at the end of tank profile url, please only enter the ID number")
    await ctx.send(f"<@{authorid}> check your DMs")

    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)
    msg = await client.wait_for("message", check=check, timeout=30)
    print(msg)
    tankid = msg.content
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/tank?tank_id={tankid}')
        resp = await response.json()
        tankname = resp['name']
        tankname = tankname.lower()
        print(tankname)
        otherTanks = resp['other_tanks']
       
        mycursor = mydb.cursor()
        sql = "INSERT INTO players (discord, tankid, tankname, chat_id, other_tanks) VALUES (%s, %s, %s, %s, %s)" #editing for other_tanks in database
        val = (f"{authorname}", f"{tankid}", f"{tankname}", f"{authorid}", f"{otherTanks}")
        mycursor.execute(sql, val)
        mydb.commit()
    await ctx.author.send(f"<@{authorid}> Tank **{tankname}** has been binded to your discord id\nUse``.mytank`` to showoff your tank")

@client.command(pass_context=True) #DONT FORGET TO CLOSE DATABASE CONNECTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def updatetank(ctx, *args):
    mydb = mysql.connector.connect(host="",
    user="",
    passwd="",
    database="")
    teamName = ' '.join(args) #if there is a space in the string it will create a space in the string
    authorid = ctx.message.author.id #discord user id
    authorname = ctx.message.author.name
    print(teamName)
    await ctx.author.send(f"<@{authorid}> enter your tank ID\n``hint:`` you can find your tank ID #number at the end of tank profile url, please only enter the ID number")
    await ctx.send(f"<@{authorid}> check your DMs")
    def check(msg):
        return msg.author == ctx.author and isinstance(msg.channel, discord.DMChannel)
    msg = await client.wait_for("message", check=check, timeout=30)

    tankid = msg.content
    async with aiohttp.ClientSession()as session:
        response = await session.get(f'https://tankpit.com/api/tank?tank_id={tankid}')
        resp = await response.json()
        tankname = resp['name']
        tankname = tankname.lower()
        mycursor = mydb.cursor()
        # sql = "UPDATE players SET tankname = %s WHERE tankid = %s"
        # val = (f"GeneraHealth", f"{authorname}")
        sql = f"UPDATE players SET tankname = %s WHERE chat_id = %s"
        val = (f"{tankname}", f"{authorid}")
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        mycursor.close()
    await ctx.author.send(f"<@{authorid}> Tank **{tankname}** has been binded to your discord id\nUse``.mytank`` to showoff your tank")

@client.command(pass_context=True) #DONT FORGET TO CLOSE DATABASE CONNECTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def mytank(ctx):
    mydb = mysql.connector.connect(host="",
    user="",
    passwd="",
    database="")
    COLORS = {
    'red': '<:r_:524455235188424718>',
    'blue': '<:b_:480148438487531520>',
    'purple': '<:p_:524458234803650580>',
    'orange': '<:o_:524458234694860800>',
    }
    embedColor = {
    'red': 0xff0000,
    'blue': 0x5c67ff,
    'purple': 0xbd23d1,
    'orange': 0xe68033,
    }
    authorname = ctx.message.author.name

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT discord, tankid FROM players")
    myresult = mycursor.fetchall()
    for x in myresult:
        if authorname in x:
            tankid = x[1]
            async with aiohttp.ClientSession()as session:
                response = await session.get(f'https://tankpit.com/api/tank?tank_id={tankid}')
                resp = await response.json()
                awards = award_string(resp['awards'])
                tankname = resp['name']

                team = resp['main_color'] #tank color
                embed=discord.Embed(title=f"{COLORS[team]} {tankname}#{tankid}", url=f"https://tankpit.com/tank_profile/?tank_id={tankid}", description=f"{awards}", color=embedColor[team])
                embed.set_footer(text='tankpit.com')
                try:
                    time = resp["map_data"]["World"]["time_played"]
                except:
                    embed.set_footer(text="Players 'World' Stats 'time played' not set to public")
                try:
                    ranks = resp["map_data"]["World"]["rank"]
                except:
                    embed.set_footer(text="Players 'World' Stats 'rank' not set to public")
                try:
                    kills = resp["map_data"]["World"]["destroyed_enemies"]
                    deac = resp ["map_data"]["World"]["deactivated"]
                    ratio = kills / deac
                    kd =(round(ratio, 2))
                except:
                    embed.set_footer(text="Players 'World' Stats 'kills' not set to public")
                    kd = "\u200b"
                try:
                    deac = resp ["map_data"]["World"]["deactivated"]
                except:
                    embed.set_footer(text="Players 'World' Stats 'deactivated' not set to public")
                lastplayed =  resp.get("last_played", "\u200b")
                favm = resp.get("favorite_map", "\u200b")
                bftank= resp.get("bf_tank_name", "\u200b")
                pong = resp.get("ping", "\u200b")
                location = resp.get("country", "\u200b")
                Bio = resp.get("profile", "\u200b")
                tptank = resp.get("name", "\u200b")
                space ="\u200b"
                try:
                    cups = resp['user_tournament_victories'] ['bronze']
                except KeyError:
                    a = "<:B_Cup_New:476303841562853377>x0"
                try:
                    cups1 = resp['user_tournament_victories'] ['silver']
                except:
                    b= "<:S_Cup_New:476303857924833290>x0"
                try:
                    cups2 = resp['user_tournament_victories'] ['gold']
                except:
                    c = "<:G_Cup_New:476303868486221824>x0"

                try:
                    embed.add_field(name="Time Played", value=f'{time}{space}', inline=True)
                except:
                    embed.add_field(name="Time Played", value="\u200b", inline=True)
                try:
                    embed.add_field(name="Rank", value=f'{ranks}{space}', inline=True)
                except:
                    embed.add_field(name="Rank", value=f'\u200b', inline=True)
                try:
                    embed.add_field(name="Kills", value=f'{kills}{space}', inline=True)
                except:
                    embed.add_field(name="Kills", value='\u200b', inline=True)
                try:
                    embed.add_field(name="Deaths", value=f'{deac}{space}', inline=True)
                except:
                    embed.add_field(name="Deaths", value='\u200b', inline=True)
                try:
                    total = cups + cups1 + cups2
                    embed.add_field(name=f"Total Cups#{total}", value=f'<:B_Cup_New:476303841562853377>x{cups}<:S_Cup_New:476303857924833290>x{cups1}<:G_Cup_New:476303868486221824>x{cups2}{space}', inline=True)
                except:
                    embed.add_field(name=f"Total Cups", value=f"{a}{b}{c}", inline=True)
                embed.add_field(name="Last played", value=resp.get("last_played", "\u200b"), inline=True)
                embed.add_field(name="K/D Ratio", value=kd, inline=True)
                mydb.commit()
                mycursor.execute(f"SELECT discord, repscore FROM players")
                myresult = mycursor.fetchall()
                for x in myresult:
                    if authorname in x:
                        rep = x[1]
                        print(tankid)
                        embed.add_field(name="Field Reputation", value=f"{rep}", inline=False)

                await ctx.send(embed=embed)
                mydb.commit()


@client.command(pass_context=True) #DONT FORGET TO CLOSE DATABASE CONNECTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
async def repboard(ctx):
    mydb = mysql.connector.connect(host="",
    user="",
    passwd="",
    database="")
    COLORS = {
    'red': '<:r_:524455235188424718>',
    'blue': '<:b_:480148438487531520>',
    'purple': '<:p_:524458234803650580>',
    'orange': '<:o_:524458234694860800>',
    }
    embedColor = {
    'red': 0xff0000,
    'blue': 0x5c67ff,
    'purple': 0xbd23d1,
    'orange': 0xe68033,
    }
    embed=discord.Embed(title=f" ", url=f" ", description=f" ")
    mycursor = mydb.cursor()
    sql = "SELECT * FROM players ORDER BY repscore DESC"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    lengthLB = (len(myresult))
    placing = ""
    for x in range(lengthLB):
        number= (x+1)
        placing += str(number) + "\n"
    embed_message = ""
    embed_message2 = ""
    for x in myresult:
        ass = (len(x))
        tanknames = (x[1])
        repscores = (x[4])
        # print(tanknames, repscores)
        embed_message += str(tanknames) + "\n"
        embed_message2 += str(repscores) + "\n"
    # for i in range(1, lengthLB):
    #     print(i)
    #     num = str(i)
    embed = discord.Embed(title=f"Reputation Leaderboard", description="",  color =0x4CBB17)
    embed.set_thumbnail(url='https://tankpit.com/images/icons/classy.png')
    embed.add_field(name="Placing", value=f"{placing}", inline=True)
    embed.add_field(name="Players", value=f"{embed_message}", inline=True)
    embed.add_field(name="Rep Score", value=embed_message2, inline=True)
    # embed.add_field(name="Reputation Rank", value=f"{rank}", inline=True)
    # embed.add_field(name="", value=embed_message, inline=False)
    await ctx.send(embed=embed)
    mydb.commit()
    mycursor.close()
   
#================MODERATION===========================================================================
@client.command(pass_context=True)
async def clear(ctx, amount=1):
    if ctx.message.author.server_permissions.manage_messages:
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.send("Messages deleted")

#================EVENTS================================================================================
@client.event
#update DemoTable set Score=Score+1 where Id=3;
async def on_message(message):
    if message.content.startswith('+'):
        mydb = mysql.connector.connect(host="",
        user="",
        passwd="",
        database="")
        authorname = message.author.name
        if message.author == client.user:
            return
        numValue = message.content #number value
        unit = message.content # rep and tank name
        # print(message)
        rep = numValue[0:2]
        # print(rep)
        rep2  = numValue[0:2]
        # print(rep2)
        # print(rep2)
        tankname = (unit[3:].lower())
        # if authorname in message.author.name:
        #     self = await client.fetch_user(message.author.id)
        #     await self.send("Sorry, you can't give reputation to yourself.")
        #     return
        if rep2 in message.content:
            tankrep = rep2.replace("+","")
        tankrep = tankrep.replace(" ","")
        # print(tankrep)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM players")
        myresult = mycursor.fetchall()
        for x in myresult:
            if tankname in x:
                # print(x[3])
                score = x[4]
                # print(x[5])
                sql = f"UPDATE players SET repscore = %s + {tankrep} WHERE tankname = %s"
                val = (f"{score}", f"{x[3]}")
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                user = await client.fetch_user(int(x[5])) #gets the discord id field in the mysql database its at the 5 index
                await user.send(f"Tankpit HQ member **{authorname}** has given your tank {tankname} **+ {tankrep} reputation points** for playing honorably on the field")
    await client.process_commands(message)



client.run(TOKEN)
