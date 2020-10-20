import random
from typing import List

from asyncpg import Record
from discord.ext import commands
from discord.ext.commands import Context


class GamblerCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db = kwargs.pop('db')

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def gamble(self, ctx: Context, amount=0):
        result: List[Record] = await self.db.fetch('SELECT * FROM users WHERE USER_ID=$1 AND SERVER_ID=$2',
                                                   f'{ctx.author.id}',
                                                   f'{ctx.guild.id}')
        points = int(result[0]["points"])
        if not isinstance(amount, int):
            await ctx.send(f'Gramy obstawiając liczbami naturalnymi, {ctx.author.name}')
            return
        if points == 0:
            await ctx.send(f'{ctx.author.name}, nie masz czym grać...')
            return
        elif amount < 0:
            await ctx.send(f'{ctx.author.name}, proszę tu nie cwaniaczkować')
        else:
            if amount == 0:
                if random.choice(['double', 'zero']) == 'double':
                    points *= 2
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(
                        f'Va banque! Brawo {ctx.author.name}, podwajasz swoje punkty i masz ich teraz {points}!')
                else:
                    await self.db.execute('UPDATE users SET POINTS=0 WHERE USER_ID=$1 AND SERVER_ID=$2',
                                          f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'Va banque! Niestety, {ctx.author.name}, ale tracisz wszystkie punkty...')
            elif amount <= points:
                if random.choice(['double', 'zero']) == 'double':
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points + amount, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'{ctx.author.name} wszedł pewniaczek i ma teraz {points + amount} punktów!')
                else:
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points - amount, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'{ctx.author.name} nie wszedł pewniaczek i ma teraz {points - amount} punktów...')
            elif amount > points:
                await ctx.send(f'{ctx.author.name} nie cwaniakuj, nie masz tyle punkcików')

    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            user = self.bot.get_user(ctx.author.id)
            await user.send(f'Masz cooldown na !gamble. Jeszcze {error.retry_after} s')
