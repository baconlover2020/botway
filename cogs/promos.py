
import discord
from discord.ext import commands
from permissions import is_adm, is_ceo
from painel.painel import dar_emblema, dar_promo_points, enviar_currency
from painel.remover_emblema import remover_emblema

def setup(bot):
    bot.add_cog(Info(bot))

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_adm()
    async def pagarpromo(self, ctx, *, args):
        try:
            args = args.split(' ')
            emblema = args[0]
            args = args[1:]
            nomes = []
            for nome in args:
                dar_emblema(nome.strip(' '), emblema)
                dar_promo_points(nome, "1")
                nomes.append(nome)
            embed = discord.Embed(title="Emblema e 1 promo point enviado aos jogadores: ")
            for nome in nomes:
                embed.add_field(name=f"{nome}: ", value=emblema)
            await ctx.message.channel.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command(aliases=["daremblema"])
    @is_adm()
    async def daremblemas(self, ctx, *, args):
        try:
            args = args.split(' ')
            emblema = args[0]
            args = args[1:]
            nomes = []
            for nome in args:
                dar_emblema(nome.strip(' '), emblema)
                nomes.append(nome)
            embed = discord.Embed(title=f"Emblema {emblema} enviado aos users:")
            for nome in nomes:
                embed.add_field(name=f"{nome}: ", value=emblema)
            await ctx.message.channel.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command()
    @is_ceo()
    async def pagamentomensal(self, ctx, *, users):
        moedas = 0
        diamantes = 10000
        duckets = 1000
        users = users.split(' ')
        embed = discord.Embed(title="Users pagos: ")
        for user in users:
            await enviar_currency(user, moedas, diamantes, duckets)
            embed.add_field(name=user, value=f"Diamantes: {str(diamantes)} duckets: {str(duckets)}")
        return await ctx.message.channel.send(embed=embed) 


    @commands.command()
    @is_adm()
    async def removeremblema(ctx, codigo, username):
        return await ctx.message.channel.send(remover_emblema(username, codigo))