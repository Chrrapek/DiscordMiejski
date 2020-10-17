import random
import os
import asyncpg
import asyncio

from discord.ext.commands import Context, bot

from miejski import Miejski
from discord.ext import commands


async def run():
    db = await asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL'))
    bot = Bot(db=db)
    try:
        await bot.start(os.environ.get('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="!"
        )
        self.db = kwargs.pop('db')

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        # await self.get_channel(271732666653474826).send("Jestem od teraz w nowej wersji!")

    @commands.command(name="miejski")
    async def miejski(self, ctx: Context):
        print('Recieved command !miejski from ' + ctx.author.name + ', processing...')
        await self.db.execute(
            'insert into users values(default, $1, $2, $3, 0) on conflict (server_id, user_id) do update set points = (select points from users where server_id=$1 and user_id=$2)+1;',
            ctx.guild.id, ctx.author.id, ctx.author.name)
        print('Executed database stuff')
        await ctx.send(await Miejski.get_message())

    @commands.command(name="stats")
    async def stats(self, ctx: Context):
        print('Recieved stats request, processing...')
        result = await self.db.fetch('select USER_NAME, POINTS from users where SERVER_ID=$1 order by POINTS desc;', ctx.guild.id)
        await ctx.send(await Miejski.get_stats(result))

    @commands.command(name="choose")
    async def choose(self, ctx, *choices: str):
        await ctx.send(random.choice(choices))


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
