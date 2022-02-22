# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import os
import os.path
from pathlib import Path
from keep_alive import keep_alive
from replit import db

token = os.environ['token']
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def leaderboard(ctx):
    await ctx.send("coming soon tm")


bot.run(token)
keep_alive()
#colon_three_copium_counts.close()