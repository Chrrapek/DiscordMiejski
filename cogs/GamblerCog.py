import random

from discord.ext import commands
from discord.ext.commands import Context


class GamblerCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db = kwargs.pop('db')

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def gamble(self, ctx: Context, amount=0):
        result = await self.db.fetch('SELECT POINTS FROM users WHERE USER_ID=$1 AND SERVER_ID=$2', f'{ctx.author.id}',
                                     f'{ctx.guild.id}')
        points = result["points"]
        if points == 0:
            await ctx.send(f'{ctx.author.id}, nie masz czym grać...')
            return
        else:
            if amount == 0:
                if random.choice(['double', 'zero']) == 'double':
                    points *= 2
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(
                        f'Va banque! Brawo {ctx.author.id}, podwajasz swoje punkty i masz ich teraz {points}!')
                else:
                    await self.db.execute('UPDATE users SET POINTS=0 WHERE USER_ID=$1 AND SERVER_ID=$2',
                                          f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'Va banque! Niestety, {ctx.author.id}, ale tracisz wszystkie punkty...')
            elif amount <= points:
                if random.choice(['double', 'zero']) == 'double':
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points + amount, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'{ctx.author.id} wszedł pewniaczek i ma teraz {points + amount} punktów!')
                else:
                    await self.db.execute('UPDATE users SET POINTS=$1 WHERE USER_ID=$2 AND SERVER_ID=$3',
                                          points - amount, f'{ctx.author.id}', f'{ctx.guild.id}')
                    await ctx.send(f'{ctx.author.id} nie wszedł pewniaczek i ma teraz {points - amount} punktów...')
            elif amount > points:
                await ctx.send(f'{ctx.author.id} nie cwaniakuj, nie masz tyle punkcików')
