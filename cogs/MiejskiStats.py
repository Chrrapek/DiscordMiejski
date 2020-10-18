from discord.ext import commands
from discord.ext.commands import Context

from miejski import Miejski


class MiejskiStats(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db = kwargs.pop('db')

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def stats(self, ctx: Context):
        print('Recieved stats request, processing...')
        result = await self.db.fetch('select USER_NAME, POINTS from users where SERVER_ID=$1 order by POINTS desc;', f'{ctx.guild.id}')
        await ctx.send(Miejski.get_stats(result))
