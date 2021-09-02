import discord
from discord.ext import commands
import shutil
import os
from painel.adicionar_categoria import adicionar_categoria
from painel.painel import adicionar_catalog_icon, buscar_categoria_por_nome, update, update_catalog_icon
from painel.scraping import id_categoria
from painel.ids import get_icon_id
import permissions
import config

 
def setup(bot):
    bot.add_cog(AdicionarCategoria(bot))

class AdicionarCategoria(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addcategoria, adicionarcategoria, adicionar_categoria, add_categoria'])
    @permissions.in_correct_channel(config.canais_furni)
    @permissions.is_adm()
    async def adicionarCategoria(self, ctx):
        for attachment in ctx.message.attachments:
                await attachment.save(f"{'temp'}/{attachment.filename}")
                message = await ctx.message.channel.send(f"⬇️ Baixando: {attachment.filename} ⬇️")
        categoria = attachment.filename
        await message.edit(content=f"⚙️ Descompactando: {categoria}... ⚙️")
        if categoria.endswith(".zip"):
            shutil.unpack_archive(os.path.join('temp', categoria), 'temp')
            os.remove(os.path.join('temp', categoria))
        if categoria.endswith(".rar"):
            os.system(f"unar -f -o {os.path.abspath('temp')} {os.path.join('temp', categoria)}")
            os.remove(os.path.join('temp', categoria))
        categoria = categoria.strip('.rar').strip('.zip').replace('_', ' ')
        for pasta in os.listdir('temp'):
            if os.path.isdir(os.path.join('temp', categoria)):
                await message.edit(content=f"⌛ Adicionando Categoria: {pasta}... ⌛")
                log, furnidata = adicionar_categoria(os.path.join('temp', pasta))
                shutil.rmtree(os.path.join('temp', pasta), ignore_errors=True)
                await message.edit(content=f"✅ A categoria \"{pasta}\" foi adicionada com êxito! ✅")
                with open(f'logs/{pasta}.txt', 'w') as f:
                    f.write(log)
                    logFile = discord.File(open(f'logs/{pasta}.txt', 'rb'))
                await ctx.message.channel.send(file=logFile)
                with open(f'logs/{pasta}-furnidata.xml', 'w') as f:
                    f.write(furnidata)
                    furnidataFile = discord.File(open(f'logs/{pasta}-furnidata.xml', 'rb'))
                await ctx.message.channel.send(file=furnidataFile)
            else:
                embed = discord.Embed(title="Categoria não encontrada.", description="Verifique se o nome do rar/zip está"
                                                                                    " identico ao da pasta.")
                embed.add_field(name="Tentei adicionar:", value=categoria)
                embed.add_field(name="Pastas recebidas:", value=os.listdir('temp'))
                await ctx.message.channel.send(embed=embed)


    @commands.command()
    @permissions.is_ceo()
    async def mobiemblema(self, ctx, _id, codigo):
        await update('catalog_items', _id, 'badge_id', codigo)
        await ctx.message.channel.send(f"Emblema {codigo} adicionando ao mobi {_id}")


    @commands.command()
    @permissions.is_adm()
    @permissions.in_correct_channel(config.canais_icon)
    async def novoicone(self, ctx, *, categoria):
        print(f"Buscando {categoria}")
        html = buscar_categoria_por_nome(categoria)
        try:
            catalog_id = id_categoria(html)[0]
            icon_id = get_icon_id()
            path = os.path.join('temp', f"icon_{icon_id}.png")
            await ctx.message.attachments[0].save(path)
            adicionar_catalog_icon(path)
            os.remove(path)
            update_catalog_icon(catalog_id, icon_id)
            print(icon_id)
            await ctx.message.channel.send(f'O icone foi adicionado com sucesso na {categoria} (id: {catalog_id}')
        except Exception as e:
            print(e)
            print(html)
            await ctx.message.channel.send("Não consegui encontrar a categoria :c")


    @commands.command()
    @permissions.is_adm()
    @permissions.in_correct_channel(config.canais_furni)
    async def movercategoria(ctx, *args):
        if len(args) == 2:
            child, parent, child_pos, parent_pos = args[0], args[1], 1, 1
        if len(args) == 3:
            if args[1].isnumeric():
                child, child_pos, parent, parent_pos = args[0], args[1], args[2], 1
            if args[2].isnumeric():
                child, parent, parent_pos, child_pos,  = args[0], args[1], args[2], 1
        if len(args) == 4:
            child, child_pos, parent, parent_pos = args[0], args[1], args[2], args[3]
        child_id = id_categoria(buscar_categoria_por_nome(child))[int(child_pos)-1]
        parent_id = id_categoria(buscar_categoria_por_nome(parent))[int(parent_pos)-1]
        update("catalog_pages", child_id, "parent_id", parent_id)
        await ctx.message.channel.send(f"{child} movido para {parent}")
        if len(args) > 4:
            return await ctx.message.channel.send(f"Parâmetros Inválidos D;")

