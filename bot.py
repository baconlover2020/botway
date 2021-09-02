import os
import asyncio
from discord.ext import commands
from config import botToken
from painel.painel import login


bot = commands.Bot(command_prefix='!')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.event
async def on_ready():
    bot.loop.create_task(login_keep_alive())


async def login_keep_alive():
    while True:
        login()
        await asyncio.sleep(3600)



bot.run(botToken)