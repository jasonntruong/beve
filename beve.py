import discord
import os
import asyncio

from discord.ext import commands, tasks
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system

from dotenv import load_dotenv

load_dotenv()