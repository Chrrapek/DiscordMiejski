from discord.ext import commands
from discord.ext.commands import Context

from miejski import Miejski


class MiejskiRandomWord(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db = kwargs.pop('db')

    @commands.command()
    async def miejski(self, ctx: Context):
        print('Recieved command !miejski from ' + ctx.author.name + ', processing...')
        await self.db.execute(
            'insert into users values(default, $1, $2, $3, 1) on conflict (server_id, user_id) do update set points = (select points from users where server_id=$1 and user_id=$2)+1;',
            f'{ctx.guild.id}', f'{ctx.author.id}', f'{ctx.author.name}')
        print('Executed database stuff')
        await ctx.send(await Miejski.get_message())