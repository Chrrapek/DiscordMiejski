import asyncio

from discord.ext import commands

from controllers.MiejskiController import Miejski


class GuessCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command(name="zabawa")
    async def guess(self, ctx, *delay_in_s: str):
        delay = 15
        if len(delay_in_s) > 0:
            try:
                delay = int(delay_in_s[0])
                if delay > 120:
                    await ctx.send(
                        "Chyba masz nierówno pod sufitem, żeby dawać taki delay. Nie słucham takiego gówna.")
                    return
            except:
                await ctx.send("Podaj samą liczbę sekund, bez żadnego s czy innego gówna")

        message = await Miejski.get_message()
        if message.has_example():
            await ctx.send(message.example_to_string())
            await asyncio.sleep(delay)
            await ctx.send(message.to_string_without_example())
        else:
            await ctx.send("No i chuj, bo haslo nie ma przykladu")
