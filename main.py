# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import os
import os.path
import json
from pathlib import Path
from keep_alive import keep_alive
from replit import db

c3_stats = 'c3_cnt'
wordle_stats_ = 'wordle_stats'


token = os.environ['token']
description = '''A lovely bot that keeps track of the number of colon threes a user sends as well as having a Wordle leaderboard.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents, case_insensitive=True)

class LeaderBoardPosition:
    def __init__(self, user, count):
        self.user = user
        self.count = count

#num_games, best_score, total_tries
class WordleLeaderBoardPosition:
    def __init__(self, user, wordle_stats):
        self.user = user
        self.num_games = wordle_stats[0]
        self.average = wordle_stats[2] / wordle_stats[0]
        self.best_score = wordle_stats[1]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#@bot.command(brief='Temp command to transfer stats into new format', description='Temp command to transfer stats into new format, depricated.')
#async def transfer_stats(ctx):
#  keys = db.keys()
#  for k in keys:
#    value = db[k]
#    print(value, type(value))
#    db[k] = dict()
#    db[k][c3_stats] = value
#  await ctx.send('done transfering info')  
  
@bot.command(brief='Leaderboard of :3', description='Leaderboard of :3 usages')
async def leaderboard(ctx):
  keys = db.keys()
  leaderboard_list = []
  for k in keys:
    values = db[k]
    if c3_stats in values.keys():
      leaderboard_list.append(LeaderBoardPosition(k, values[c3_stats]))
  top = sorted(leaderboard_list, key=lambda x: x.count, reverse=True)
  em = discord.Embed(title=f":3 Leaderboard <:copium:856725125507186708>",     description="<:copium:856725125507186708> Leaderboard of most usages of :3 <:copium:856725125507186708>")
  for i in range(len(top)):
    user = top[i].user
    name = await bot.fetch_user(user)
    value = top[i].count
    em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
  await ctx.send(embed=em)
  
@bot.command(brief='Show your :3 count', description='Show your :3 count')
async def count(ctx):
  userID = ctx.author.id
  userID_string = '<@!' + str(userID) + '>'
  userID = str(userID)
  try:
    user_total = int(db[userID][c3_stats])
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

@bot.command(brief='Get Leaderboard of Average Wordle Scores', description='Get Leaderboard of Average Wordle Scores, Best SCore feature coming soon tm')
async def wordle(ctx):
  keys = db.keys()
  leaderboard_list = []
  for k in keys:
    values = db[k]
    if wordle_stats_ in values.keys() and values[wordle_stats_][0] > 0:
      leaderboard_list.append(WordleLeaderBoardPosition(k, values[wordle_stats_]))
  top = sorted(leaderboard_list, key=lambda x: x.average)
  em = discord.Embed(title=f"Wordle Leaderboard",     description="Leaderboard of Average Wordle Scores!")
  for i in range(len(top)):
    user = top[i].user
    name = await bot.fetch_user(user)
    value = top[i].average
    em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
  await ctx.send(embed=em)

#@bot.command()
#async def resetWordle(ctx):
#  for k in db.keys():
#    db[k][wordle_stats_] = [0, 999, 0]
  
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
  userID = str(message.author.id)
  userID_string = '<@!' + userID + '>'
  msg = message.content
  #count number of :3
  cnt = 0
  for i in range(len(msg) - 1):
    if (msg[i:i + 2] == ':3'):
      if (i + 2 >= len(msg) or msg[i + 2 : i + 3] == ' ' \
        or msg[i + 2 : i + 3] == '3') \
        and (i - 1 == -1 or msg[i - 1 : i] != ':'):
          cnt += 1
  if cnt > 0:
    
    try:
      user_total = int(db[userID][c3_stats]) + cnt
    except:
      user_total = cnt
    if userID not in db.keys() or type(db[userID] != dict()):
        db[userID] = dict()
    db[userID][c3_stats] = user_total
    bot_message = "colon three <:copium:856725125507186708>"
    await message.channel.send(bot_message)
    await message.add_reaction('<:copium:856725125507186708>')
    
  #wordle
  if msg.startswith('Wordle'):
    idx = msg.index('/')
    if (msg[idx - 1:idx].lower() == 'x'):
      await message.add_reaction('<:pepega:861280783968894987>')
    else:
      num_tries = int(msg[idx - 1:idx])
      try:
        user_wordle_stats = db[userID][wordle_stats_]
      except:
        user_wordle_stats = [0, 999, 0]
      #update
      user_wordle_stats[0] += 1
      user_wordle_stats[1] = min(num_tries, user_wordle_stats[1])
      user_wordle_stats[2] += num_tries
      if userID not in db.keys() or type(db[userID] != dict()):
        db[userID] = dict()
      db[userID][wordle_stats_] = [user_wordle_stats[0], user_wordle_stats[1], user_wordle_stats[2]]
      if (num_tries < 3):
        await message.add_reaction('<:poggies:748558867272695819>')
      else:
        await message.add_reaction('<:pepepoint:748563096616042618>')
    
keep_alive()    
bot.run(token)
