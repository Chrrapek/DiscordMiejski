import random
import discord
import os

from discord.ext.commands import Context
from utils import Utils
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.get_channel(271732666653474826).send("Jestem od teraz w nower wersji!")


@bot.command()
async def miejski(ctx: Context):
    print('Recieved command !miejski from ' + ctx.author.name + ', processing...')
    await ctx.send(await Utils.get_message())


@bot.command(description='Pomoc w decyzjach')
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))


bot.run(os.environ.get('DISCORD_TOKEN'))
