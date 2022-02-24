import discord
from discord.ext import commands
from replit import db
from main import wordle_stats_

#num_games, best_score, total_tries
class WordleLeaderBoardPosition:
    def __init__(self, user, wordle_stats):
        self.user = user
        self.num_games = wordle_stats[0]
        self.average = wordle_stats[2] / wordle_stats[0]
        self.best_score = wordle_stats[1]

class Wordle(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(brief='Get Leaderboard of Average Wordle Scores', description='Get Leaderboard of Average Wordle Scores, Best SCore feature coming soon tm', help='Displays leaderboard of average wordle scores')
  async def wordle(self, ctx):
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
      name = await self.bot.fetch_user(user)
      value = top[i].average
      em.add_field(name=f"{str(i + 1)}. {name}", value=f"{value}", inline=False)
    await ctx.send(embed=em)
  
  #@bot.command()
  #async def resetWordle(ctx):
  #  for k in db.keys():
  #    db[k][wordle_stats_] = [0, 999, 0]

def setup(bot: commands.Bot):
    bot.add_cog(Wordle(bot))