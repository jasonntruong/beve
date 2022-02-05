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
import sys
import random

sys.path.insert(0, '/home/pi/beve/FaceRecognition')

from facialrec import getFace

load_dotenv()

botJSON = open("/home/pi/beve/data.json", "r+")
botData = json.load(botJSON)
TOKEN = botData["token"]

send = False
announcement = ""
serverMembers = set()
pomoOn = True

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='beve ')

oldChapo = [360233756738584576, 297555807200083988]

channelName = {327597608111570947: "D", 820371352694947850: "zuck ma dong", 888863361268326490: "meanie beanie", 756191311505391627: "York bois", 756676813920403496: "Demon Time", 893392467968282735: "Sleep Date", 902716252139687946: "study date", 937599329567391744: "Sad boy hour"}

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
        await asyncio.sleep(60)

#HOROSCOPE
@client.command(brief="Enter your zodiac and get your daily horoscope")
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

#MBTI
@client.command(brief="Enter your MBTI and get a description")
async def mbti(ctx):
    messages = ctx.message.content.split(" ")
    mbti = messages[2].lower()
    
    await ctx.send(file=discord.File('/home/pi/beve/MBTI/'+mbti.lower()+'.jpg'))

@client.event
async def on_message(message):
    imgExt = ["png", "jpg", "jpeg"]

    if message.content == ('beve sees'):
        if any(message.attachments[0].filename.lower().endswith(ext) for ext in imgExt):
            await message.attachments[0].save("/home/pi/beve/FaceRecognition/imageToDetect.png")
            await message.channel.send("Yo " + message.author.display_name + ",\n" + getFace(False))
    
    if message.content == ('beve sees all'):
        if any(message.attachments[0].filename.lower().endswith(ext) for ext in imgExt):
            await message.attachments[0].save("/home/pi/beve/FaceRecognition/imageToDetect.png")
            await message.channel.send("Yo " + message.author.display_name + ",\n" + getFace(True))

    else:
        await client.process_commands(message)

#POMODORO
@client.command(brief="start pomodoro; beve pomostart workTime breakTime")
async def pomostart(ctx):
    global pomoOn
    pomoOn = pomoOn
    working = True
    time = 0

    messages = ctx.message.content.split(" ")
    workTime = int(messages[2])
    breakTime = int(messages[3])

    await ctx.author.edit(deafen=True)
    await ctx.author.edit(mute=True)

    while time < workTime:
        if pomoOn:
            await asyncio.sleep(1)
            time += 1
        else:
            pomoOn = True
            await ctx.author.edit(deafen=False)
            await ctx.author.edit(mute=False)
            return

    await ctx.author.edit(deafen=False)
    await ctx.author.edit(mute=False)
    await asyncio.sleep(breakTime)
    await pomostart(ctx)

@client.command(brief="stop pomodoro")
async def pomostop(ctx):
    global pomoOn
    pomoOn = False

#ROULETTE
@client.command(brief="beve randomnly deafens someone for 5-10 seconds")
async def roulette(ctx):
    if ctx.author.id in oldChapo:
        allConnectedMembers = ctx.author.voice.channel.members
        
        unluckyMember = random.choice(allConnectedMembers)
        time = random.randint(5, 10)

        await ctx.send(unluckyMember.display_name + " has been chosen. Enjoy the silent void for " + str(time) + " seconds")
        await unluckyMember.edit(deafen=True)
        await unluckyMember.edit(mute=True)

        await asyncio.sleep(time)

        await unluckyMember.edit(deafen=False)
        await unluckyMember.edit(mute=False)

#BUS
@client.command(brief="beve takes you on a bus trip")
async def bus(ctx):
    route = []
    allVC = botData["chats"]["allVoiceID"]

    userVC = ctx.author.voice.channel.id
    indexVC = allVC.index(userVC)
    routeMsg = "Our route: "

    for i in range (indexVC+1, len(allVC)):
        route.append(allVC[i])
        routeMsg += channelName[allVC[i]] + " -> "
    
    for i in range (0, indexVC+1):
        route.append(allVC[i])
        routeMsg += channelName[allVC[i]] + " -> "
    
    await ctx.send(routeMsg[:-4])
    for i in range(len(route)):
        vc = client.get_channel(route[i])
        await ctx.author.move_to(vc)
        await asyncio.sleep(2)

#PICK
@client.command(brief="picks a RNRandomness Valorant agent")
async def pick(ctx):
    allVal = ["Astra", "Breach", "Brimstone", "Cypher", "Jett", "KAY/O", "Killjoy", "Omen", "Phoenix", "Raze", "Reyna", "Sage", "Skye", "Sova", "Viper", "Yoru", "Chamber", "Neon"]

    await ctx.send("**" + str(ctx.message.author.display_name) +  "** got: " + allVal[random.randrange(0,len(allVal))])

client.run(TOKEN)