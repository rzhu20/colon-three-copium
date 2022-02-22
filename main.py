# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import os
import os.path
import json
from pathlib import Path
from keep_alive import keep_alive
from replit import db


token = os.environ['token']
description = '''A lovely bot that keeps track of the number of colon threes a user sends as well as having a Wordle leaderboard.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


user_stats = None
user_stats_file = Path("user_counter.json")
if user_stats_file.is_file():
  user_counter = json.load(open("user_counter.json"))
else:
  user_counter = {}

class LeaderBoardPosition:
    def __init__(self, user, count):
        self.user = user
        self.count = count

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def leaderboard(ctx):
  keys = db.keys()
  leaderboard_list = []
  for k in keys:
    value = db[k]
    leaderboard_list.append(LeaderBoardPosition(k, value))
  top = sorted(leaderboard_list, key=lambda x: x.count, reverse=True)
  em = discord.Embed(title=f":3 Leaderboard <:copium:856725125507186708>",     description="<:copium:856725125507186708> Leaderboard of most usages of :3 <:copium:856725125507186708>")
  for i in range(len(top)):
    user = top[i].user
    name = await bot.fetch_user(user)
    value = top[i].count
    em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
  await ctx.send(embed=em)
  
@bot.command()
async def count(ctx):
  userID = ctx.author.id
  userID_string = '<@!' + str(userID) + '>'
  userID = str(userID)
  try:
    user_total = int(db[userID])
  except:
    user_total = 0
  if type(user_total) != int or user_total == 0:
    bot_message = "<:poggies:748558867272695819> " + userID_string + " has never used :3!"
  elif user_total == 1:
    bot_message = "colon three <:copium:856725125507186708>\n" + userID_string + " has only used :3 1 time <:sadge:827995795596116030>"
  elif user_total <= 50:
    bot_message = "colon three <:copium:856725125507186708>\n" + userID_string + " has only used :3 " + str(user_total) + " times <:sadge:827995795596116030>"
  elif user_total <= 100:
    bot_message = "colon three <:copium:856725125507186708>\n" + userID_string + " has used :3 " + str(user_total) + " times!"
  elif user_total <= 500:
    bot_message = "colon three <:copium:856725125507186708>\n" + userID_string + " has used :3 a whopping " + str(user_total) + " times! <:pepega:861280783968894987>"
  else:
    bot_message = "colon three <:copium:856725125507186708>\n" + userID_string + " has used :3 " + str(user_total) + " times! Woman is that you?<:womanhappy:814749175031136266>"
  await ctx.send(bot_message)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content[0] == '!':
    try:
      await bot.process_commands(message)
    except:
      await message.channel.send("Invalid Command!")
      return
  userID = message.author.id
  userID_string = '<@!' + str(userID) + '>'
  msg = message.content
  cnt = 0
  for i in range(len(msg) - 1):
    if (msg[i:i + 2] == ':3'):
      if (i + 2 >= len(msg) or msg[i + 2 : i + 3] == ' ' \
        or msg[i + 2 : i + 3] == '3') \
        and (i - 1 == -1 or msg[i - 1 : i] != ':'):
          cnt += 1
  if cnt > 0:
    userID = str(userID)
    try:
      user_total = int(db[userID]) + cnt
    except:
      user_total = cnt
    db[userID] = user_total
    bot_message = "colon three <:copium:856725125507186708>"
    await message.channel.send(bot_message)
    await message.add_reaction('<:copium:856725125507186708>')
bot.run(token)
keep_alive()
#colon_three_copium_counts.close()