import asyncio
import os

import asyncpg
import praw
from cogs.MemoryCog import MemoryCog
from discord.ext import commands

from cogs.ChooseCog import ChooseCog
from cogs.GamblerCog import GamblerCog
from cogs.GuessCog import GuessCog
from cogs.HelpCog import HelpCog
from cogs.MiejskiCog import MiejskiCog
from cogs.RabbinCog import RabbinCog
from cogs.RedditCog import RedditCog
from controllers.DatabaseController import DatabaseController
from praw.models import Subreddit


async def run():
    pool = await asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL'))
    db = DatabaseController(pool)
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_APP_NAME'),
        client_secret=os.environ.get('REDDIT_SECRET'),
        user_agent="ChrapBot by u/Chramar"
    ).subreddit("hmmm")
    bot = Bot(db, reddit)
    try:
        await bot.start(os.environ.get('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, db: DatabaseController, reddit_instance: Subreddit, **kwargs):
        super().__init__(
            command_prefix='!'
        )
        self.add_cog(MiejskiCog(self, db=db))
        self.add_cog(RedditCog(self, reddit_instance=reddit_instance))
        self.add_cog(ChooseCog(self))
        self.add_cog(GamblerCog(self, db=db))
        self.add_cog(HelpCog(self))
        self.add_cog(GuessCog(self))
        self.add_cog(RabbinCog(self))
        self.add_cog(MemoryCog())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        await self.get_channel(271732666653474826).send("Jestem od teraz w nowej wersji!")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
