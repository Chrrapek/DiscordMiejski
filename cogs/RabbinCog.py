from discord.ext import commands
from discord.ext.commands import Context

from controllers.YesNoController import YesNoController
from utils.ErrorMessages import ErrorMessages


class RabbinCog(commands.Cog):

    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command()
    async def rabbin(self, ctx: Context):
        print('Recieved command !rabbin from ' + ctx.author.name + ', processing...')
        await ctx.send(YesNoController.get_response())

    @rabbin.error
    async def rabbin_error(self, ctx, error):
        print(f'Error wywolany przez {ctx.author.name}: {error}')
        await ctx.send(ErrorMessages.get_random_error_message())
