import discord
from discord.ext import commands
from replit import db
from main import c3_stats

class LeaderBoardPosition:
    def __init__(self, user, count):
        self.user = user
        self.count = count

class C3Commands(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(brief='Leaderboard of :3', description='Leaderboard of :3 usages', help='Displays leaderboard of :3 usages')
  async def leaderboard(self, ctx: commands.Context):
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
      name = await self.bot.fetch_user(user)
      value = top[i].count
      em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
    await ctx.send(embed=em)
    
  @commands.command(brief='Shows your :3 count', description='Shows your :3 count', help='Shows your :3 count')
  async def count(self, ctx: commands.Context):
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

def setup(bot: commands.Bot):
    bot.add_cog(C3Commands(bot))