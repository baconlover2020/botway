import os
from discord.ext import commands
from config import botToken
from painel.painel import login


bot = commands.Bot(command_prefix='!')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.event
async def on_ready():
    pass
    #login()



bot.run(botToken)