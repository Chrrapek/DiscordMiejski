from discord.ext import commands
from discord.ext.commands import Context
from praw.models import Subreddit
import random


class RedditCog(commands.Cog):
    def __init__(self, bot, reddit_instance: Subreddit):
        self.bot = bot
        self.reddit_instance = reddit_instance

    @commands.command(name="hmmm-top")
    async def hmmm_top(self, ctx: Context):
        print('Recieved /r/hmmm request, processing...')
        top = [post for post in self.reddit_instance.top("week")]
        random.shuffle(top)
        selected_post = top[0]
        await ctx.send(selected_post.url)

    @commands.command()
    async def hmmm(self, ctx: Context):
        print('Recieved /r/hmmm request, processing...')
        selected_post = self.reddit_instance.random()
        await ctx.send(selected_post.url)
