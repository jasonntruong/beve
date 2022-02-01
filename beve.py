import discord
import os
import asyncio

from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system

from dotenv import load_dotenv

load_dotenv()

tokenFile = open("token.txt", "r")
TOKEN = tokenFile.read()

client = commands.Bot(command_prefix = 'beve.')

@client.event
async def on_ready():
    print('Beve is logged in')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="RnBeve"))

@client.event
async def on_message(message):
    # await client.process_commands(message)

    if message.content == 'beve.hi':
        await message.channel.send('hi')

client.run(TOKEN)