from discord.ext import commands


class MemoryCog(commands.Cog):
    def __init__(self, **kwargs):
        self.n = 0

    @commands.command()
    async def memory(self, ctx, amount=0):
        if not isinstance(amount, int):
            await ctx.send("Turlaj dropsa")
            return
        self.n = self.n + amount
        await ctx.send(f"Mam {self.n}")
