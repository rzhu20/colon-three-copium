import discord
import json
import os
import os.path
from pathlib import Path
from keep_alive import keep_alive
from replit import db


token = os.environ['token']

client = discord.Client()
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

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
      return
  
  userID = message.author.id
  userID_string = '<@!' + str(userID) + '>'
  msg = message.content
  cnt = 0
  if (msg == '!leaderboard'):
    keys = db.keys()
    leaderboard_list = []
    for k in keys:
      value = db[k]
      leaderboard_list.append(LeaderBoardPosition(k, value))
    top = sorted(leaderboard_list, key=lambda x: x.count, reverse=True)
    em = discord.Embed(title=f":3 Leaderboard <:copium:856725125507186708>", description="<:copium:856725125507186708> Leaderboard of most usages of :3 <:copium:856725125507186708>")
    for i in range(len(top)):
      user = top[i].user
      name = await client.fetch_user(user)
      value = top[i].count
      em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
    await message.channel.send(embed=em)
    return

  elif (msg == '!count'):
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
    await message.channel.send(bot_message)
    return
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
    # json.dump(user_counter, open(colon_three_copium_counts, 'w'))
    #print(cnt, user_total)
    db[userID] = user_total
    bot_message = "colon three <:copium:856725125507186708>"
    await message.channel.send(bot_message)
    await message.add_reaction('<:copium:856725125507186708>')
    

      #print(msg)
  elif (msg[:6] == 'Wordle'):
    score = int(msg[msg.index('/') - 1])
    userID = str(userID)
    try:
      user_stats = (db[userID]) #average, best, total, number_of_games
    except:
      user_stats = [0, 0, 0]
    print(type(user_stats))
    if score < int(user_stats[1]) or int(user_stats[1]) == 0:
      user_stats[1] = score
    user_stats[2] += score
    user_stats[3] += 1
    user_stats[0] = user_stats[2] / user_stats[3]
    if score < 3:
      await message.add_reaction('<:945717627517546536>')
    elif score <=5:
      await message.add_reaction('945717731842474064')
    else:
      await message.add_reaction('945717843054436402')
    
keep_alive()
client.run(token)
colon_three_copium_counts.close()

