import asyncio
import os

import asyncpg
import discord
import praw
from discord.ext import commands

from cogs.ChooseCog import ChooseCog
from cogs.DuelCog import DuelCog
from cogs.GamblerCog import GamblerCog
from cogs.GuessCog import GuessCog
from cogs.HelpCog import HelpCog
from cogs.MiejskiCog import MiejskiCog
from cogs.RabbinCog import RabbinCog
from cogs.RedditCog import RedditCog
from controllers.DatabaseController import DatabaseController
from praw.models import Subreddit


async def run():
    pool = await asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL')+'?sslmode=require')
    db = DatabaseController(pool)
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_APP_NAME'),
        client_secret=os.environ.get('REDDIT_SECRET'),
        user_agent="ChrapBot by u/Chramar"
    ).subreddit("hmmm")
    intents = discord.Intents.default()
    intents.members = True
    bot = Bot(db, reddit, intents)
    try:
        await bot.start(os.environ.get('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, db: DatabaseController, reddit_instance: Subreddit, intents,  **kwargs):
        super().__init__(
            command_prefix='!',
            intents=intents
        )
        self.add_cog(MiejskiCog(self, db=db))
        self.add_cog(RedditCog(reddit_instance))
        self.add_cog(ChooseCog(self))
        self.add_cog(GamblerCog(self, db=db))
        self.add_cog(HelpCog(self))
        self.add_cog(GuessCog(self))
        self.add_cog(RabbinCog(self))
        self.add_cog(DuelCog(db=db, name_extractor=self.extract_user_name))

    def extract_user_name(self, user_id):
        user = self.get_user(int(user_id))
        return user.name

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        await self.get_channel(271732666653474826).send("Jestem od teraz w nowej wersji!")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
