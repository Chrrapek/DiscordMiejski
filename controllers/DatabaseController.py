from typing import List

from asyncpg import Record


class DatabaseController:
    def __init__(self, db):
        self.db = db

    def close(self):
        self.db.close()

    async def upsert_user_points(self, server_id: str, author_id: str, author_name: str, points: int):
        print('Upserting user points')
        await self.db.execute(
            'insert into users values(default, $1, $2, $3, $4) on conflict (server_id, user_id) do update set points=$4;',
            server_id, author_id, author_name, points)
        print('Executed upsert')

    async def fetch_users_points(self, server_id: str):
        print('Fetching user points')
        result = await self.db.fetch('select USER_NAME, POINTS from users where SERVER_ID=$1 order by POINTS desc;',
                                     server_id)
        print('Executed database stuff')
        return result

    async def fetch_user_points(self, user_id: str, server_id: str) -> int:
        result: List[Record] = await self.db.fetch('SELECT * FROM users WHERE USER_ID=$1 AND SERVER_ID=$2',
                                                   user_id,
                                                   server_id)
        if len(result) > 0:
            return int(result[0]["points"])
        else:
            return 0
