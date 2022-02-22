import discord
import json
import os
import os.path
from pathlib import Path
from keep_alive import keep_alive
from replit import db
from discord.ext import commands


bot = commands.Bot(command_prefix='$')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    
keep_alive()

