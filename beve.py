from discord.ext import commands, tasks
from discord.utils import get
from os import system
from dotenv import load_dotenv
from datetime import datetime

import discord
import os
import asyncio
import requests
import json

load_dotenv()

botJSON = open("data.json", "r+")
botData = json.load(botJSON)
TOKEN = botData["token"]

send = False
announcement = ""
serverMembers = set()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='beve ')

#GENERAL FUNCTIONS
def editJSON(key, data):
    botData[key] = data
    botJSON.seek(0)
    json.dump(botData, botJSON)
    botJSON.truncate()

#DISCORD FUNCTIONS
@client.event
async def on_ready():
    global serverMembers

    main_text = client.get_channel(botData["chats"]["main_text"])
    #main_text = client.get_channel(botData["chats"]["bot_spam"]) switch to when testing features

    print('Beve is logged in')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="RnBeve"))

    for guild in client.guilds:
        for member in guild.members:
            serverMembers.add(member)

    animeReminder.start(main_text)

#ANIME REMINDER
@tasks.loop(hours=24)
async def animeReminder(channel):
    global send, announcement
    if send:
        send = False
        await channel.send(announcement)

@animeReminder.before_loop
async def before_animeReminder():
    global send, announcement, serverMembers
    await client.wait_until_ready()
    for i in range(60*24):
        now = datetime.now()
        current_time = now.strftime("%w:%H:%M")
        print(current_time)
        for anime in botData["animes"]:
            if current_time == anime["date"]:
                announcement = "**NEW EPISODE FOR " + anime["name"] + " OUT NOW!!**\n--------------------------------------------------\n\n"
                announcement += "WATCH IT HERE: " + anime["link"] + "\n\n"

                for member in anime["ping"]:
                    for serverMember in serverMembers:
                        if member == str(serverMember):
                            print(serverMember)
                            announcement += "{} ".format(serverMember.mention)
                
                send = True
                return
        await asyncio.sleep(60)

#HOROSCOPE
@client.command(brief="Enter your birthday MM/DD and get your daily horoscope")
async def horoscope(ctx):
    zodaicToNum = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
    messages = ctx.message.content.split(" ")
    zodiac = messages[2].lower()

    #web scrape
    URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + str(zodaicToNum.index(zodiac)+1)
    horoscopePage = requests.get(URL)

    #since no ID for the actual horoscope
    startOfHoro = horoscopePage.text.split("</strong>")
    endOfHoro = startOfHoro[1].split("</p>")
    
    await ctx.send("**" + ctx.author.display_name.upper() + "'S HOROSCOPE FOR TODAY**\n" + endOfHoro[0][3:])


@client.event
async def on_message(message):
    await client.process_commands(message)
    # if message.content == 'beve.hi':
    #     await message.channel.send('hi')

client.run(TOKEN)