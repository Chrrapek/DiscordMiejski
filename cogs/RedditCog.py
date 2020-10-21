from discord.ext import commands
from discord.ext.commands import Context


class RedditCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.reddit_instance = kwargs.pop('reddit_instance')

    @commands.command()
    async def hmmm(self, ctx: Context):
        print('Recieved /r/hmmm request, processing...')
        selected_post = self.reddit_instance.random()
        await ctx.send(selected_post.url)
