from discord.ext import commands
import discord
import os
import shutil
import painel
from scraping import get_online_staffs, get_online_amb, id_categoria
import adicionar_cor
import furni_search
from variables import bot_token, users, channels

bot = commands.Bot(command_prefix='!')
temp = 'temp'


def can_add_furni():
    def predicate(ctx):
        for user in users:
            if user.id == ctx.message.author.id and user.can_add_furni():
                return True
        return False
    return commands.check(predicate)


def can_add_badge():
    def predicate(ctx):
        for user in users:
            if user.id == ctx.message.author.id and user.can_add_badge:
                return True
        return False
    return commands.check(predicate)


def is_in_correct_channel():
    def predicate(ctx):
        for channel_id in channels:
            if ctx.message.channel.id == channel_id:
                return True
        return False
    return commands.check(predicate)


def is_admin():
    def predicate(ctx):
        for user in users:
            if user.id == ctx.message.author.id and user.is_admin:
                return True
        return False
    return commands.check(predicate)



@bot.event
async def on_ready():
    painel.login()



@bot.command()
@commands.check_any(is_admin(), can_add_furni())
async def addcategoria(ctx):
    painel.check_login()
    for attachment in ctx.message.attachments:
            await attachment.save(f"{temp}/{attachment.filename}")
            await ctx.message.channel.send(f"Baixando: {attachment.filename}")
    categoria = attachment.filename
    if categoria.endswith(".zip"):
        await ctx.message.channel.send(f"Descompactando: {categoria}")
        shutil.unpack_archive(os.path.join(temp, categoria), temp)
        os.remove(os.path.join(temp, categoria))
    if categoria.endswith(".rar"):
        await ctx.message.channel.send(f"Descompactando: {categoria}")
        os.system(f"unar -f -o {os.path.abspath(temp)} {os.path.join(temp, categoria)}")
        os.remove(os.path.join(temp, categoria))
    categoria = categoria.strip('.rar').strip('.zip').replace('_', ' ')
    for pasta in os.listdir("temp"):
        if verificar_coerencia(categoria, pasta):
            categoria = pasta
    if os.path.isdir(os.path.join(temp, categoria)):
        await ctx.message.channel.send(f"Adicionando Categoria: {categoria}")
        await painel.adicionar_categoria(os.path.join(temp, categoria), ctx.message)
        shutil.rmtree(os.path.join(temp, categoria), ignore_errors=True)
        await ctx.message.channel.send(f"A categoria \"{categoria}\" foi adicionada com êxito!")
    else:
        embed = discord.Embed(title="Categoria não encontrada.", description="Verifique se o nome do rar/zip está"
                                                                             " identico ao da pasta.")
        embed.add_field(name="Tentei adicionar:", value=categoria)
        embed.add_field(name="Pastas recebidas:", value=os.listdir(temp))
        await ctx.message.channel.send(embed=embed)


@bot.command()
@commands.check_any(is_admin(), can_add_furni())
async def addcatalogicon(ctx):
    painel.check_login()
    _id = painel.get_icon_id()
    path = os.path.join(temp, f"icon_{_id}.png")
    await ctx.message.attachments[0].save(path)
    await painel.adicionar_catalog_icon(path, ctx.message)
    os.remove(path)
    return _id


@bot.command()
@commands.check_any(is_admin())
async def addcores(ctx, nome, cor1, cor2=''):
    cor1 = cor1.replace('#', '')
    cor2 = cor2.replace('#', '')
    if cor2 == '':
        cor2 = cor1
    icon_path = await adicionar_cor.criar_gif(cor1, cor2)
    await adicionar_cor.hospedar_cor(nome, cor1, cor2, message=ctx.message)
    _file = discord.File(icon_path)
    embed = discord.Embed(title='Cor(es) adicionada(s): ')
    embed.add_field(name='Nome:', value=nome, inline=False)
    embed.add_field(name='Cor 1:', value=cor1, inline=False)
    embed.add_field(name='Cor 2:', value=cor2, inline=False)
    embed.set_image(url=f"attachment://temp/{icon_path}")
    await ctx.message.channel.send(file=_file, embed=embed)

@bot.command()
@commands.check_any(is_admin(), can_add_furni())
async def novoicone(ctx, *, categoria):
    painel.check_login()
    print(f"Buscando {categoria}")
    html = painel.buscar_categoria_por_nome(categoria)
    try:
        catalog_id = id_categoria(html)[0]
        icon_id = await addcatalogicon(ctx)
        await painel.update_catalog_icon(catalog_id, icon_id, message=ctx.message)
    except Exception as e:
        print(e)
        print(html)
        await ctx.message.channel.send("Não consegui encontrar a categoria :c")


@bot.command()
@commands.check_any(is_admin(), can_add_badge())
async def addemblema(ctx, cod, nome, desc, _url=None):
    painel.check_login()
    if len(ctx.message.attachments) > 0:
        url = ctx.message.attachments[0].url
    elif _url is not None:
        url = _url
    else:
        return
    painel.hospedar_emblema1(url, cod, nome, desc)
    embed = discord.Embed(title="Emblema Hospedado!", color=discord.Color.dark_orange())
    embed.set_image(url=url)
    embed.add_field(name="Código: ", value=cod, inline=False)
    embed.add_field(name="Título: ", value=nome, inline=False)
    embed.add_field(name="Descrição: ", value=desc, inline=False)
    os.remove(os.path.join("temp", cod + '.gif'))
    await ctx.message.channel.send(embed=embed)

@bot.command()
@commands.check_any(is_admin(), can_add_badge())
async def daremblema(ctx, nome, emblema):
    painel.check_login()
    nome, emblema = painel.dar_emblema(nome, emblema)
    embed = discord.Embed(title="Emblema enviado: ")
    embed.add_field(name="Emblema:", value=emblema)
    embed.add_field(name="Jogador:", value=nome)
    await ctx.message.channel.send(embed=embed)

@bot.command()
@commands.check_any(is_admin(), can_add_badge())
async def pagarpromo(ctx, *, args):
    painel.check_login()
    try:
        args = args.split(' ')
        emblema = args[0]
        args = args[1:]
        nomes = []
        for nome in args:
            painel.dar_emblema(nome.strip(' '), emblema)
            painel.dar_promo_points(nome, "1")
            nomes.append(nome)
        embed = discord.Embed(title="Emblema e 1 promo point enviado aos jogadores: ")
        for nome in nomes:
            embed.add_field(name=f"{nome}: ", value=emblema)
        await ctx.message.channel.send(embed=embed)
    except Exception as e:
        print(e)


@bot.command()
@commands.check_any(is_admin(), can_add_badge())
async def daremblemas(ctx, *, args):
    painel.check_login()
    try:
        args = args.split(' ')
        emblema = args[0]
        args = args[1:]
        nomes = []
        for nome in args:
            painel.dar_emblema(nome.strip(' '), emblema)
            nomes.append(nome)
        embed = discord.Embed(title=f"Emblema {emblema} enviado aos users:")
        for nome in nomes:
            embed.add_field(name=f"{nome}: ", value=emblema)
        await ctx.message.channel.send(embed=embed)
    except Exception as e:
        print(e)


@bot.command()
@commands.check_any(is_admin())
async def mobiemblema(ctx, _id, codigo):
    painel.check_login()
    await painel.update('catalog_items', _id, 'badge_id', codigo, message=ctx.message)
    await ctx.message.channel.send(f"Emblema {codigo} adicionando ao mobi {_id}")


@commands.check_any(is_admin(), can_add_furni(), can_add_badge(), is_in_correct_channel())
@bot.command()
async def buscarmobi(ctx, *, mobi):
    painel.check_login()
    await ctx.message.channel.send(f"Aguarde... Buscando mobi: '{mobi}'...")
    furnis = furni_search.find_key(mobi)
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




@commands.check_any(is_admin(), can_add_furni(), can_add_badge(), is_in_correct_channel())
@bot.command()
async def staffinfo(ctx):
    pag_staff = painel.buscar_equipe()
    staffs = get_online_staffs(pag_staff)
    pag_amb = painel.buscar_amb()
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


@bot.command()
@commands.check_any(is_admin(), can_add_furni())
async def movercategoria(ctx, *args):
    painel.check_login()
    if len(args) == 2:
        child, parent, child_pos, parent_pos = args[0], args[1], 1, 1
    if len(args) == 3:
        if args[1].isnumeric():
            child, child_pos, parent, parent_pos = args[0], args[1], args[2], 1
        if args[2].isnumeric():
            child, parent, parent_pos, child_pos,  = args[0], args[1], args[2], 1
    if len(args) == 4:
        child, child_pos, parent, parent_pos = args[0], args[1], args[2], args[3]
    child_id = id_categoria(painel.buscar_categoria_por_nome(child))[int(child_pos)-1]
    parent_id = id_categoria(painel.buscar_categoria_por_nome(parent))[int(parent_pos)-1]
    await painel.update("catalog_pages", child_id, "parent_id", parent_id, ctx.message)
    await ctx.message.channel.send(f"{child} movido para {parent}")
    if len(args) > 4:
        return await ctx.message.channel.send(f"Parâmetros Inválidos D;")


@commands.check_any(is_admin(), can_add_furni(), can_add_badge())
@bot.command()
async def comandos(ctx):
    embed = discord.Embed(title="Comandos: ")
    embed.add_field(name="!addcategoria", value="Envie o comando com uma categoria em forma zip ou rar.", inline=False)
    embed.add_field(name='!addemblema "código" "nome" "desc" "url" ',
                    value='url opcional, pode enviar uma imagem também. Utilize as aspas', inline=False)
    embed.add_field(name="!novoicone categoria", value="Envie o icone desejado junto com o comando", inline=False)
    embed.add_field(name="!buscarmobi nome do mobi",
                    value="Mostra a categoria de determinado mobi (utilize o nome exato)", inline=False)
    embed.add_field(name="!staffinfo", value="Mostra os membros da equipe online no momento.", inline=False)
    embed.add_field(name="!movercategoria \"categoria\" \"categoria_parent\"",
                    value="Move a primeira categoria escolhida para dentro da segunda categoria escolhida", inline=False)
    embed.add_field(name="!daremblema jogador codigo",
                    value="Da o emblema escolhido ao jogador. (precisa relogar pra aparecer)", inline=False)
    embed.add_field(name="!daremblemas codigo jogador1 jogador2 etc",
                    value="Da o emblema escolhido aos jogadores selecionados. (precisa relogar pra aparecer)", inline=False)
    embed.add_field(name="!pagarpromo codigo jogador1 jogador2 etc",
                    value="Da o emblema escolhido e 1 age coin aos jogadores selecionados. (precisa relogar pra aparecer)", inline=False)
    embed.add_field(name="!addcores \"nome da cor \" hex_da_cor1 hex_da_cor_2",
                    value="Adiciona as cores escolhidas a aba cores de nome vip", inline=False)
    embed.add_field(name="!mobiemblema catalog_id codigo",
                    value="Adiciona um emblema ao mobi selecionado (ltd)", inline=False)
    await ctx.message.channel.send(embed=embed)


def verificar_coerencia(categoria, pasta):
    counter = 0
    for c, letra in enumerate(categoria.lower()):
        try:
                counter += int(letra == pasta.lower()[c])
        except:
            pass
    if counter >= len(categoria) - 2:
        return True
    else:
        return False

bot.run(bot_token)
