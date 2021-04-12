import random

from discord.ext import commands
from discord.ext.commands import Context

from controllers.DatabaseController import DatabaseController
from utils.ErrorMessages import ErrorMessages
from utils.emoji import PEPE_SAD, PEPE_NAWROCKI


class GamblerCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db: DatabaseController = kwargs.pop('db')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def gamble(self, ctx: Context, amount=0):
        points = await self.db.fetch_user_points(f'{ctx.author.id}', f'{ctx.guild.id}')
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
                multiplier = random.choice([0, 2])
                if multiplier == 0:
                    await ctx.send(self.va_banque_lose_message(ctx.author.name))
                else:
                    await ctx.send(
                        f'Va banque! Brawo {ctx.author.name}, podwajasz swoje punkty i masz ich teraz {points * multiplier}!')
                points *= multiplier
                await self.db.upsert_user_points(f'{ctx.guild.id}', f'{ctx.author.id}', f'{ctx.author.name}', points)
            elif amount <= points:
                if random.choice([0, 2]) == 2:
                    new_points = points + amount
                    await self.db.upsert_user_points(f'{ctx.guild.id}', f'{ctx.author.id}', f'{ctx.author.name}',
                                                     new_points)
                    await ctx.send(self.win_message(ctx.author.name, new_points))
                else:
                    new_points = points - amount
                    await self.db.upsert_user_points(f'{ctx.guild.id}', f'{ctx.author.id}', f'{ctx.author.name}',
                                                     new_points)
                    await ctx.send(self.lose_message(ctx.author.name, new_points))
            elif amount > points:
                await ctx.send(f'{ctx.author.name} nie cwaniakuj, nie masz tyle punkcików')

    def va_banque_lose_message(self, name):
        return f'Va banque! Niestety, {name}, ale tracisz wszystkie punkty...' + str(self.bot.get_emoji(PEPE_SAD))

    def lose_message(self, name, new_points):
        return f'{name} nie wszedł pewniaczek i ma teraz {new_points} punktów... ' + str(self.bot.get_emoji(PEPE_SAD))

    def win_message(self, name, new_points):
        return f'{name} wszedł pewniaczek i ma teraz {new_points} punktów! ' + str(self.bot.get_emoji(PEPE_NAWROCKI))

    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.author.send(f'Masz cooldown na !gamble. Jeszcze {error.retry_after} s')
        else:
            print(f'Error wywolany przez {ctx.author.name}: {error}')
            await ctx.send(ErrorMessages.get_random_error_message())
