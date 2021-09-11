import discord
from discord.ext import commands
from painel.adicionar_emblema import EmblemaExistente, UrlInvalido, hospedar_emblema, verificarDuplicadosPorUrl
import permissions
import config
 

def setup(bot):
    bot.add_cog(HospedarEmblema(bot))

class HospedarEmblema(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["adicionarEmblema", "hospedar_emblema", "adicionar_emblema", "addemblema", "adicionaremblema"])
    @permissions.is_adm()
    @permissions.in_correct_channel(config.canais_emblema)
    async def hospedarEmblema(self, ctx, cod, nome, desc, _url=None):
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif _url is not None:
            url = _url
        else:
            return
        embed = discord.Embed(title="⚙️ Verificando disponibilidade ⚙️", color=discord.Color.blue())
        embed.set_image(url=url)
        embed.add_field(name="Código: ", value=cod, inline=False)
        embed.add_field(name="Título: ", value=nome, inline=False)
        embed.add_field(name="Descrição: ", value=desc, inline=False)
        msg = await ctx.message.channel.send(embed=embed)
        duplicados =verificarDuplicadosPorUrl(url, cod)
        if duplicados:
            embed = discord.Embed(title="Existem emblemas semelhantes a esse.\nDeseja prosseguir?", color=discord.Color.gold())
            embed.set_image(url=url)
            embed.add_field(name="Código: ", value=cod, inline=False)
            embed.add_field(name="Título: ", value=nome, inline=False)
            embed.add_field(name="Descrição: ", value=desc, inline=False)
            for duplicado in duplicados:
                embed.add_field(name="Código do emblema semelhante: ", value=duplicado.strip('.gif'), inline=False)
            await msg.edit(embed=embed)
            await msg.add_reaction('✅')
            return await msg.add_reaction('❌')
        try:
            hospedar_emblema(url, cod, nome, desc)
        except UrlInvalido:
            embed = msg.embeds[0]
            embed.title = "Erro - Link inválido"
            embed.color = discord.Color.red()
            return await msg.edit(embed=embed)
        except EmblemaExistente:
            embed = msg.embeds[0]
            embed.title = "Erro - Esse código ja foi utilizado. Tente novamente"
            embed.color = discord.Color.red()
            return await msg.edit(embed=embed)
        embed = discord.Embed(title="Emblema Hospedado!", color=discord.Color.green())
        embed.set_image(url=url)
        embed.add_field(name="Código: ", value=cod, inline=False)
        embed.add_field(name="Título: ", value=nome, inline=False)
        embed.add_field(name="Descrição: ", value=desc, inline=False)
        await ctx.message.channel.send(embed=embed)


    @commands.command()
    @permissions.is_embaixador()
    @permissions.in_correct_channel(config.canais_emblema)
    async def solicitaremblema(self, ctx, cod, nome, desc, evento, _url=None):
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif _url is not None:
            url = _url
        else:
            return
        embed = discord.Embed(title="⚙️ Verificando disponibilidade ⚙️", color=discord.Color.blue())
        embed.set_image(url=url)
        embed.add_field(name="Código: ", value=cod, inline=False)
        embed.add_field(name="Título: ", value=nome, inline=False)
        embed.add_field(name="Descrição: ", value=desc, inline=False)
        embed.add_field(name="Evento: ", value=evento, inline=False)
        embed.add_field(name="Solicitado por: ", value=ctx.message.author.mention, inline=False)
        msg = await ctx.message.channel.send(embed=embed)
        duplicados = verificarDuplicadosPorUrl(url, cod)
        if duplicados:
            embed = discord.Embed(title="Existem emblemas semelhantes. Por favor utilize um emblema inédito!", color=discord.Color.red())
            embed.set_image(url=url)
            for duplicado in duplicados:
                embed.add_field(name="Código do emblema semelhante: ", value=duplicado.strip('.gif'), inline=False)
            return await msg.edit(embed=embed)
            
        embed = discord.Embed(title="Solicitação de Emblema", color=discord.Color.gold())
        embed.set_image(url=url)
        embed.add_field(name="Código: ", value=cod, inline=False)
        embed.add_field(name="Título: ", value=nome, inline=False)
        embed.add_field(name="Descrição: ", value=desc, inline=False)
        embed.add_field(name="Evento: ", value=evento, inline=False)
        embed.add_field(name="Solicitado por: ", value=ctx.message.author.mention, inline=False)
        await msg.edit(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, reacter):
        if reaction.message.author.id == self.bot.user.id and not reacter.id == self.bot.user.id:
            if permissions.aceitar_emblema(reacter.roles):
                if reaction.emoji == '✅':
                    try:
                        embed = reaction.message.embeds[0]
                        if 'olicitação' in embed.title:
                            embed.title = "⌛ Hospedando..."
                            embed.color = discord.Color.blue()
                            cod, nome, desc, evento, solicitante = embed.fields
                            cod, nome, desc, evento, solicitante = cod.value, nome.value, desc.value, evento.value,solicitante.value,
                            url = embed.image.url
                            await reaction.message.edit(embed=embed)
                        elif 'emblemas semelhantes' in embed.title:
                            embed.title = "⌛ Hospedando..."
                            embed.color = discord.Color.blue()
                            cod, nome, desc = embed.fields[0], embed.fields[1], embed.fields[2]
                            cod, nome, desc = cod.value, nome.value, desc.value,
                            url = embed.image.url
                            await reaction.message.edit(embed=embed)
                    except:
                        return
                    try:
                        hospedar_emblema(url, cod, nome, desc)
                    except UrlInvalido:
                        embed = reaction.message.embeds[0]
                        embed.title = "Erro - Link inválido"
                        embed.color = discord.Color.red()
                        return await reaction.message.edit(embed=embed)
                    except EmblemaExistente:
                        embed = reaction.message.embeds[0]
                        embed.title = "Erro - Esse código ja foi utilizado. Tente novamente"
                        embed.color = discord.Color.red()
                        return await reaction.message.edit(embed=embed)

                    embed = discord.Embed(title="Emblema Aprovado!", color=discord.Color.green())
                    embed.set_image(url=url)
                    embed.add_field(name="Código: ", value=cod, inline=False)
                    embed.add_field(name="Título: ", value=nome, inline=False)
                    embed.add_field(name="Descrição: ", value=desc, inline=False)
                    if evento:
                        embed.add_field(name="Nome do evento: ", value=evento, inline=False)
                        embed.add_field(name="Solicitado por: ", value=solicitante, inline=False)
                        embed.add_field(name="Aprovado por: ", value=reacter.mention, inline=False)
                    await reaction.message.edit(embed=embed)
                if reaction.emoji == '❌' and not reacter.id == self.bot.user.id:
                    return await reaction.message.delete()
            return
        return 


    