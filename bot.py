import random
import os
import asyncpg

from discord.ext.commands import Context

from miejski import Miejski
from discord.ext import commands


bot = commands.Bot(command_prefix='!')
db = asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL'))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.get_channel(271732666653474826).send("Jestem od teraz w nowej wersji!")


@bot.command()
async def miejski(ctx: Context):
    print('Recieved command !miejski from ' + ctx.author.name + ', processing...')
    await db.execute(
        'insert into users values(default, $1, $2, $3, 0) on conflict (server_id, user_id) do update set points = (select points from users where server_id=$1 and user_id=$2)+1;',
        ctx.guild.id, ctx.author.id, ctx.author.name)
    print('Executed database stuff')
    await ctx.send(await Miejski.get_message())


@bot.command()
async def stats(ctx: Context):
    print('Recieved stats request, processing...')
    result = await db.fetch('select USER_NAME, POINTS from users where SERVER_ID=$1 order by POINTS desc;', ctx.guild.id)
    await ctx.send(await Miejski.get_stats(result))


@bot.command(description='Pomoc w decyzjach')
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))


bot.run(os.environ.get('DISCORD_TOKEN'))
