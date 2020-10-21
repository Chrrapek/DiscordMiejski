import time

from discord.ext import commands

from miejski import Miejski

delay_in_s = 15


class GuessCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command(name="zabawa")
    async def guess(self, ctx):
        message = await Miejski.get_message()
        if message.has_example():
            await ctx.send(message.example_to_string())
            time.sleep(delay_in_s)
            await ctx.send(message.to_string_without_example())
        else:
            await ctx.send("No i chuj, bo haslo nie ma przykladu")


