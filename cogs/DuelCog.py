from random import Random

import discord
from discord.ext import commands

from cogs.duel.DuelArena import DuelArena, DuelStatus
from controllers.DatabaseController import DatabaseController


class DuelCog(commands.Cog):
    def __init__(self, db: DatabaseController, **kwargs):
        self.db = db
        self.arena = DuelArena(Random())

    @commands.command(name="duel-list")
    async def duel_list(self, ctx):
        challenger_id = str(ctx.author.id)
        server_id = str(ctx.guild.id)
        rivals = self.arena.list_user_waiting_duels_rivals(server_id, challenger_id)
        open_duels = self.arena.list_user_open_duels_rivals(server_id, challenger_id)
        formatted_opened = "\n".join(open_duels)
        formatted_rivals = "\n".join([f"`!duel @{rival}`" for rival in rivals])
        message = f"Tu czekasz: \n" \
                  f"{formatted_opened}\n" \
                  f"Tu czekają na Ciebie:\n" \
                  f"{formatted_rivals}" \
                  f""
        await ctx.send(message)

    @commands.command()
    async def duel(self, ctx, target: discord.User, prize: int = 0):
        challenger_id = str(ctx.author.id)
        challenger_name = str(ctx.author.name)
        target_name = str(target.name)
        server_id = str(ctx.guild.id)
        target_id = str(target.id)
        challenger_points = await self.db.fetch_user_points(challenger_id, server_id)
        target_points = await self.db.fetch_user_points(target_id, server_id)
        if challenger_points < prize:
            await ctx.send("Panie kolego, nie ma tak")
            return
        if target_points < prize:
            await ctx.send("Cel jest zabyt biedny")
            return
        if not self.arena.reverse_proposal_exists(server_id, challenger_id, target_id) and prize < 1:
            await ctx.send("Panie kolego, nie ma tak")
            return

        duel_result = self.arena.add_or_make_duel(server_id, challenger_id, prize, target_id)
        if duel_result.status == DuelStatus.DUEL_CREATED:
            await ctx.send("Walka czeka")
            return
        if duel_result.status == DuelStatus.CANNOT_DUEL_WITH_YOURSELF:
            await ctx.send("Ale weź kogoś jeszcze")
            return
        if duel_result.status == DuelStatus.DUEL_ALREADY_CREATED:
            await ctx.send("Daj się najpierw raz sklepać")
            return

        if duel_result.status == DuelStatus.TARGET_WON:
            new_target_points = target_points + duel_result.prize
            new_challenger_points = challenger_points - duel_result.prize
            await self.db.upsert_user_points(server_id, target_id, target_name, new_target_points)
            await self.db.upsert_user_points(server_id, challenger_id, challenger_name, new_challenger_points)
            await self.send_result(challenger_name, ctx, new_challenger_points, new_target_points, target_name)
            return

        if duel_result.status == DuelStatus.CHALLENGER_WON:
            new_target_points = target_points - duel_result.prize
            new_challenger_points = challenger_points + duel_result.prize
            await self.db.upsert_user_points(server_id, target_id, target_name, new_target_points)
            await self.db.upsert_user_points(server_id, challenger_id, challenger_name, new_challenger_points)
            await self.send_result(target_name, ctx, new_target_points, new_challenger_points, challenger_name)
            return
        await ctx.send("Nie powinno mnie tu być")
        pass

    @staticmethod
    async def send_result(loser_name, ctx, loser_points, winner_points, winner_name):
        await ctx.send(
            f'{winner_name} pyknął {loser_name} i ma teraz {winner_points}. Przegranemu zostało tylko {loser_points}')
