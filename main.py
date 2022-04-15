# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord_components import DiscordComponents, Select, SelectOption, Button, ButtonStyle
from discord.utils import get
import os
import os.path
from keep_alive import keep_alive
from replit import db

c3_stats = 'c3_cnt'
wordle_stats_ = 'wordle_stats'

token = os.environ['token']
bot_description = '''A lovely bot that keeps track of the number of colon threes a user sends as well as having a Wordle leaderboard.'''
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
DiscordComponents(client)
bot = commands.Bot(command_prefix='!', description=bot_description, intents=intents, case_insensitive=True)

class MyHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
     
  async def send_bot_help(self, mapping):
    embed = discord.Embed(title="Help", description=bot_description)
    for cog, cmds in mapping.items():
      filtered = await self.filter_commands(cmds, sort=True)
      command_signatures = [self.get_command_signature(c) for c in filtered]
      if command_signatures:
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
    channel = self.get_destination()
    await channel.send(embed=embed)

  async def send_command_help(self, command):
    embed = discord.Embed(title=self.get_command_signature(command))
    embed.add_field(name='Help', value=command.help)
    alias = command.aliases
    if alias:
      embed.add_field(name='Aliases', value=", ".join(alias), inline=False)
    channel = self.get_destination()
    await channel.send(embed=embed)

  async def send_error_message(self, error):
    embed = discord.Embed(title='Error', description=error)
    channel = self.get_destination()
    await channel.send(embed=embed)

bot.help_command = MyHelp()

bot.load_extension('c3_cog')
bot.load_extension('wordle_cog')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


'''@bot.command()
async def button(ctx):
  await ctx.send("Hello, World!", components = [Button(label = "WOW button!", custom_id = "button1")])
  print('button.')
  interaction = await bot.wait_for("button_click", check=lambda i:i.custom_id == "button1")
  print('hi')
  await interaction.send(content = "Button clicked!")
  print('ok')
  

@bot.command()
async def select(ctx):
  await ctx.send("Hello, World!", components = [Select(placeholder = "Select something!", options = [SelectOption(label = "A", value = "A"), SelectOption(label = "B", value = "B")])])

  interaction = await bot.wait_for("select_option")
  await interaction.send(content = f"{interaction.values[0]} selected!")
'''

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    await ctx.channel.send("Invalid Command!")

@bot.event 
async def on_message(message):
  if message.author == bot.user:
    return
  if message.content and message.content[0] == '!':
    try:
      await bot.process_commands(message)
    except:
      return
  
  userID = str(message.author.id)
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
      if (num_tries <= 3):
        await message.add_reaction('<:poggies:748558867272695819>')
      else:
        await message.add_reaction('<:pepepoint:748563096616042618>')


'''class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Option 1",emoji="👌",description="This is option 1!"),
            discord.SelectOption(label="Option 2",emoji="✨",description="This is option 2!"),
            discord.SelectOption(label="Option 3",emoji="🎭",description="This is option 3!")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Option 1":
            await interaction.response.edit_message(content="This is the first option from the entire list!")
        elif self.values[0] == "Option 2":
            await interaction.response.send_message("This is the second option from the list entire wooo!",ephemeral=False)
        elif self.values[0] == "Option 3":
            await interaction.response.send_message("Third One!",ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

@bot.command()
async def menu(ctx):
    await ctx.send("Menus!",view=SelectView())
'''
  
keep_alive()    
bot.run(token)
