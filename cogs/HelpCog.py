from discord.ext import commands
from discord.ext.commands import Context


class HelpCog(commands.Cog):
    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def pomoc(self, ctx: Context):
        help_msg = f'**Pomoc:**' \
               f'\n**!miejski** - losuje słowo z miejski.pl i przydziela użytkownikowi tyle pkt ile wynosi jego ocena. Cooldown 10 minut dla użytkownika' \
               f'\n**!stats** - wyświetla liczbę punktów użytkowników serwera. Cooldown 30 sekund w ramach serwera' \
               f'\n**!gamble [wartość]** - 50% szans na podwojenie postawionej wartości, 50% na stracenie. Bez podania wartości do losowania idą wszystkie posiadane punkty użytkownika. Cooldown 10 minut dla użytkownika' \
               f'\n**!choose [opcje]** - losuje jedną z podanych opcji (opcje muszą być rozdzielone spacją)' \
               f'\n**!pomoc** - wyświetla tę pomoc. Cooldown 5 minut w ramach serwera' \
               f'\n**!zabawa** [czas w sekundach] - Zgadywanie hasła po przykładzie. Domyślna wartość czasu to 15s'

        await ctx.send(help_msg)
