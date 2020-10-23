from discord.ext import commands
from discord.ext.commands import Context

from controllers.DatabaseController import DatabaseController
from controllers.MiejskiController import Miejski


class MiejskiCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.db: DatabaseController = kwargs.pop('db')

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def miejski(self, ctx: Context):
        print('Recieved command !miejski from ' + ctx.author.name + ', processing...')
        message = await Miejski.get_message()
        await self.db.upsert_user_points(f'{ctx.guild.id}', f'{ctx.author.id}', f'{ctx.author.name}',
                                         int(message.rating))
        await ctx.send(message.to_string())

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def stats(self, ctx: Context):
        print('Recieved command !stats, processing...')
        result = await self.db.fetch_users_points(f'{ctx.guild.id}')
        await ctx.send(Miejski.get_stats(result))

    @miejski.error
    async def miejski_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            user = self.bot.get_user(ctx.author.id)
            await user.send(f'Masz cooldown na !miejski. Jeszcze {error.retry_after} s')
        else:
            print(f'Error wywolany przez {ctx.author.name}: {error}')
            await ctx.send('Sorki, wykopyrtnąłem się i gdybym miał nóżki to bym nimi machał')

