# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import os
import os.path
import random
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
async def test(ctx, arg):
    await ctx.send(arg)


bot.run(token)