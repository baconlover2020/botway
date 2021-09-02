import discord
from discord.ext import commands
from painel.buscar_mobi import buscar_mobi
from painel.painel import buscar_equipe, buscar_amb
from painel.scraping import get_online_staffs, get_online_amb
import permissions
import config

def setup(bot):
    bot.add_cog(Buscar(bot))

class Buscar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["buscarmobis", "procurarmobi", "procurarmobis"])
    @permissions.in_correct_channel(config.canais_buscar_mobi)
    async def buscarmobi(self, ctx, *, mobi):
        furnis = buscar_mobi(mobi)
        if type(furnis) != type([]):
            return await ctx.message.channel.send(furnis)
        else:
            embed = discord.Embed(title=f"Categorias encontradas para o mobi {mobi}:", desc="Busque nas seguintes categorias")
            categorias = []
            for furni in furnis:
                if furni.page_name not in categorias:
                    categorias.append(furni.page_name)
            for categoria in categorias:
                furnis_categoria = []
                for furni in furnis:
                    if furni.page_name == categoria and furni.name.title() not in furnis_categoria:
                        furnis_categoria.append(furni.name.title())
                embed.add_field(name=f"{categoria}:", value="\n".join(furnis_categoria), inline=False)
            await ctx.message.channel.send(embed=embed) 
        

    @commands.command(aliases=["infostaff"])
    async def staffinfo(self, ctx):
        pag_staff = buscar_equipe()
        staffs = get_online_staffs(pag_staff)
        pag_amb = buscar_amb()
        ambs = get_online_amb(pag_amb)
        embed = discord.Embed(title="Membros da Equipe Online:")
        ranks_on = []
        if staffs or ambs:
            for staff, rank in staffs:
                if rank not in ranks_on:
                    ranks_on.append(rank)

            for rank_on in ranks_on:
                staffs_rank = []
                string = '\n'
                for staff, rank in staffs:
                    if rank == rank_on:
                        staffs_rank.append(staff)
                embed.add_field(name=f"{rank_on.replace('Eventos', 'Promotor de Eventos')}:", value=string.join(staffs_rank),
                                inline=False)
            if ambs:
                embed.add_field(name="Embaixadores:", value=string.join(ambs))
            await ctx.message.channel.send(embed=embed)
        else:
            await ctx.message.channel.send("Nenhum membro da equipe online no momento.")