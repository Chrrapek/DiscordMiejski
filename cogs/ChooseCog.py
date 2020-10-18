import random

from discord.ext import commands


class ChooseCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command()
    async def choose(self, ctx, *choices: str):
        await ctx.send(random.choice(choices))
