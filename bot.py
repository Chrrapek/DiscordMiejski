import os
import asyncpg
import asyncio
import praw

from cogs.MiejskiRandomWord import MiejskiRandomWord
from cogs.MiejskiStats import MiejskiStats
from discord.ext import commands

from cogs.RedditHmmm import RedditHmmm


async def run():
    db = await asyncpg.create_pool(dsn=os.environ.get('DATABASE_URL'))
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_APP_NAME'),
        client_secret=os.environ.get('REDDIT_SECRET'),
        user_agent="ChrapBot by u/Chramar"
    ).subreddit("hmmm")
    bot = Bot(db=db, reddit_instance=reddit)
    try:
        await bot.start(os.environ.get('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix='!'
        )
        self.db = kwargs.pop('db')
        self.reddit_instance = kwargs.pop('reddit_instance')
        self.add_cog(MiejskiRandomWord(self, db=self.db))
        self.add_cog(MiejskiStats(self, db=self.db))
        self.add_cog(RedditHmmm(self, reddit_instance=self.reddit_instance))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        await self.get_channel(271732666653474826).send("Jestem od teraz w nowej wersji!")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
