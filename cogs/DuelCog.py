from random import Random

from discord.ext import commands

from cogs.duel.DuelArena import DuelArena
from controllers.DatabaseController import DatabaseController


class MemoryCog(commands.Cog):
    def __init__(self, db: DatabaseController, **kwargs):
        self.db = db
        self.arena = DuelArena(Random())

    @commands.command()
    async def duel(self, ctx, target: str, prise: int):
        challenger = ctx.author.name
        server_id = ctx.guild.id
        pass
