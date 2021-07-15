import requests
import os
import discord
import urllib.parse
import shutil
from variables import auth, get_id, get_icon_id, set_id
import scraping


def get_classname(swf_path):
    swf_path = swf_path.replace('\\', '/')
    return swf_path.split('/')[-1].replace('.swf', '').replace('_icon.png', '')


with requests.Session() as session:
    def login():
            print('Iniciando painel')
            session.get(auth.security_link)
            session.post('http://setoradministrativo.agehotel.info/login.php', data=auth.payload)
            scraping.verify_success(session.post('http://setoradministrativo.agehotel.info/pin.php', data=auth.pin))
    

    def adicionar_pagina(id_pagina, nome_pagina, parent_id='4242000', icon_image='10', rank='7'):
        print('Criando categoria no catalogo com ID: ' + str(id_pagina) + ' e nome: ' + nome_pagina)
        pagina = {
            'id[]': id_pagina,
            'parent_id[]': parent_id,
            'type[]': 'DEFAULT',
            'caption[]': nome_pagina,
            'icon_color[]': '1',
            'icon_image[]': icon_image,
            'visible[]': '1',
            'enabled[]': '1',
            'min_rank[]': rank,
            'club_only[]': '0',
            'order_num[]': '1',
            'page_layout[]': 'default_3x3',
            'page_images[]': '[]',
            'page_texts[]': '[]',
            'min_sub[]': '0',
            'vip_only[]': '0',
            'link[]': 'undefined',
            'extra_data[]': ''}
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-catalog-pages', data=pagina)
        print('Categoria ' + nome_pagina + ' criada com sucesso.')
        return nome_pagina


    async def adicionar_catalog_icon(catalog_item_path, message=None):
        files = {'userfile[]': open(catalog_item_path, 'rb')}
        session.post('http://setoradministrativo.agehotel.info/salvar_catalog.php', files=files)
        await message.channel.send(f"{os.path.basename(catalog_item_path)} foi hospedado em catalog.")
        return catalog_item_path


    async def adicionar_icon(icon_path, message=None):
        icon_path = icon_path.replace('\\', '/').replace('"', '')
        try:
            files = {'userfile[]': open(icon_path, 'rb')}
            session.post('http://setoradministrativo.agehotel.info/salvar_icon_catalogue.php', files=files)
            print(icon_path.split('/')[-1] + ' foi hospedado.')
            try:
                await message.channel.send(f"{icon_path.split('/')[-1]} foi hospedado.")
            except:
                await message.channel.send(f"{icon_path} foi hospedado.")
            return icon_path.split('/')[-1]
        except Exception as e:
            print(e)
            print(f"Nao foi possivel encontrar o icon {icon_path}")


    async def adicionar_icons(icons_path, message=None):
        icons_path = icons_path.replace('\\', '/').replace('"', '')
        print('---------- Hospedando Icones ----------')
        for icon in os.listdir(icons_path):
            await adicionar_icon(os.path.join(icons_path, icon), message)
        print("Todos os icones foram hospedados.")


    async def adicionar_swf(swf_path, message=None):
        swf_path = swf_path.replace('\\', '/').replace('"', '')
        files = {'userfile[]': open(swf_path, 'rb')}
        session.post('http://setoradministrativo.agehotel.info/salvar_swf2.php', files=files)
        print(swf_path.split('/')[-1] + ' foi hospedado.')
        await message.channel.send(f"{swf_path.split('/')[-1]} foi hospedado.")
        return swf_path.split('/')[-1]


    async def hospedar_attachments(message=None):
        for attachment in message.attachments:
            if attachment.filename.endswith(".swf"):
                files = {'userfile[]': await attachment.read()}
                session.post('http://setoradministrativo.agehotel.info/salvar_swf2.php', files=files)
                await message.channel.send(f"{attachment.filename} foi hospedado.")
            if attachment.filename.endswith(".png"):
                files = {'userfile[]': await attachment.read()}
                session.post('http://setoradministrativo.agehotel.info/salvar_icon_catalogue.php', files=files)
                await message.channel.send(f"{attachment.filename} foi hospedado.")


    async def adicionar_swfs(swfs_path, message=None):
        print('Hospedando SWF')
        for swf in os.listdir(swfs_path):
            await adicionar_swf(os.path.join(swfs_path, swf), message)
        print('Todas SWFs da pasta foram hospedada')


    def criar_furnidata(classname, nome, descrição, _id=get_id()):
        return f"<furnitype id=\"{str(_id)}\" classname=\"{classname}\">\n<revision>500008</revision> \n<defaultdir>0</defaultdir> \n<xdim>1</xdim> <ydim>1</ydim> \n<partcolors> <color>0</color> \n<color>0</color> <color>0</color> \n</partcolors> <name>{nome}</name> \n<description>{descrição}</description> \n<adurl/> <offerid>-1</offerid> <buyout>0</buyout> \n<rentofferid>0</rentofferid> <rentbuyout>0</rentbuyout> \n<bc>0</bc> <excludeddynamic>0</excludeddynamic> <customparams/> <specialtype>1</specialtype> \n<canstandon>0</canstandon> <cansiton>0</cansiton> <canlayon>0</canlayon> </furnitype> \n"


    def criar_furnidata_color(classname, nome, descrição, _id=get_id(), cor1="ffffff", cor2="ffffff"):
        return f"<furnitype id=\"{_id}\" classname=\"{classname}\">\n<revision>56688</revision>\n<defaultdir>0</defaultdir>\n<xdim>1</xdim>\n<ydim>1</ydim>\n<partcolors>\n<color>#{cor1.strip('#')}</color>\n<color>#{cor2.strip('#')}</color>\n</partcolors>\n<name>{nome}</name>\n<description>{descrição}</description>\n<adurl/>\n<offerid>-1</offerid>\n<buyout>0</buyout>\n<rentofferid>-1</rentofferid>\n<rentbuyout>0</rentbuyout>\n<bc>1</bc>\n<excludeddynamic>0</excludeddynamic>\n<customparams>-0.25</customparams>\n<specialtype>1</specialtype>\n<canstandon>1</canstandon>\n<cansiton>0</cansiton>\n<canlayon>0</canlayon>\n</furnitype>"


    def criar_furnidatas(swf_path, categoria):
        print(f'---------- Criando furnidata para {categoria} ----------')
        furnidata = ''
        _ids = []
        nomes = {}
        for c, swf in enumerate(os.listdir(swf_path), int(get_id())):
            nome = criar_nome(swf)
            furnidata += criar_furnidata(swf.replace('.swf', ''), nome, categoria, _id=c)
            _ids.append(c)
            nomes[c] = nome
        return furnidata, _ids, nomes


    def criar_nome(nome):
        nome = nome.replace('.swf', '').lower()
        inverter = ['habbox', 'habblet', 'habbo', 'habb', 'hab']
        for coisa in inverter:
            if coisa in nome:
                nome = nome.replace(coisa, '###')
        nome = nome.replace('_', ' ')
        palavras = nome.split(' ')
        resultado = ''
        for palavra in palavras:
            if not palavra == ' ':
                resultado += palavra.capitalize() + ' '
        return resultado.replace('###', 'Age')


    async def adicionar_furnidata(furnidata, message=None):
        data = {'furnitype': furnidata}
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-roomwcampo&table=room', data=data)
        with open(f"furnidata.xml", 'w') as f:
            f.write(furnidata)
            furnidata_file = discord.File(open('furnidata.xml', 'rb'))
        return await message.channel.send(file=furnidata_file)
        

    async def adicionar_furniture(_id, public_name='steinlindo', item_name='steinlindo', _type='s', width='1', length='1',
                            stack_heigth='0', can_stack='1', can_sit='0', is_walkable='0',
                            sprite_id='', allow_gift='0', interaction_type='default', interaction_modes_count='10', vending_ids='0',
                            effect_id='0', variable_heights='0', song_id='0', message=None):
        if sprite_id == '':
            sprite_id = _id
        furniture = {'id[]': _id, 'public_name[]': public_name, 'item_name[]': item_name, 'type[]': _type,
                     'width[]': width, 'length[]': length, 'stack_height[]': stack_heigth, 'can_stack[]': can_stack,
                     'can_sit[]': can_sit, 'is_walkable[]': is_walkable, 'sprite_id[]': sprite_id,
                     'allow_recycle[]': '1', 'allow_trade[]': '1', 'allow_marketplace_sell[]': '1',
                     'allow_gift_back[]': '1', 'allow_gift[]': allow_gift, 'allow_inventory_stack[]': '1',
                     'interaction_type[]': interaction_type, 'interaction_modes_count[]': interaction_modes_count,
                     'vending_ids[]': vending_ids, 'is_arrow[]': '0', 'foot_figure[]': '0', 'stack_multiplier[]': '0',
                     'subscriber[]': '0', 'effect_id[]': effect_id, 'variable_heights[]': variable_heights,
                     'flat_id[]': '-1', 'revision[]': '49500',
                     'description[]': 'Age', 'specialtype[]': '1', 'canlayon[]': '0', 'requires_rights[]': '1',
                     'song_id[]': song_id, 'date[]': '2020-10-04 19:31:41'}

        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-furniture', data=furniture)
        print(f"SQL adicionado: id:{_id} sprite_id:{sprite_id}")
        await message.channel.send(f"SQL adicionado: id: {_id} sprite_id: {sprite_id}")
        return furniture


    async def adicionar_furnitures(_ids, public_name='steinlindo', item_name='steinlindo', _type='s', width='1', length='1',
                            stack_heigth='0', can_stack='1', can_sit='0', is_walkable='0',
                            sprite_id='', allow_gift='1', interaction_type='default', interaction_modes_count='10', vending_ids='0',
                            effect_id='0', variable_heights='0', song_id='0', message=None):
        for _id in _ids:
            await adicionar_furniture(_id, public_name=public_name, item_name=item_name, _type=_type, width=width, length=length,
                            stack_heigth=stack_heigth, can_stack=can_stack, can_sit=can_sit, is_walkable=is_walkable,
                            sprite_id=sprite_id, allow_gift='0', interaction_type=interaction_type, interaction_modes_count=interaction_modes_count, vending_ids=vending_ids,
                            effect_id=effect_id, variable_heights=variable_heights, song_id=song_id, message=message)
        print('Todos os mobis foram adicionados ao furniture')


    async def adicionar_catalogo(page_id, item_id='', catalog_name='', cost_credits='5', cost_pixels='0', amount='1', song_id='0',
                           limited_sells='0', extradata='', badge_id='', cost_diamonds='99999999', message=None):
        catalogo = {'page_id[]': page_id,
                    'item_ids[]': item_id,
                    'catalog_name[]': catalog_name,
                    'cost_credits[]': cost_credits,
                    'cost_snow[]': '0',
                    'cost_pixels[]': cost_pixels,
                    'amount[]': amount,
                    'vip[]': '0',
                    'achievement[]': '0',
                    'song_id[]': song_id,
                    'limited_sells[]': limited_sells,
                    'limited_stack[]': '0',
                    'offer_active[]': '1',
                    'extraData[]': extradata,
                    'badge_id[]': badge_id,
                    'flat_id[]': '-1',
                    'date[]': '2020-10-04 22:00:39',
                    'cost_seasonal[]': '0',
                    'cost_diamonds[]': cost_diamonds}
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-catalog-items', data=catalogo)
        print(f"ID {item_id} adicionado a pagina {page_id} com nome {catalog_name} e qtde {amount}")
        try:
            await message.channel.send(f"ID {item_id} adicionado a pagina {page_id} com nome {catalog_name}")
        except Exception as e:
            print(e)
        return catalogo


    async def adicionar_catalogos(id_pagina, nome_pagina, _ids, cost_credits='5', cost_diamonds='9999999', nomes=None , message=None):
        for _id in _ids:
            await adicionar_catalogo(id_pagina, _id, nomes[_id], cost_credits, cost_diamonds=cost_diamonds, message=message)
        print('Todos os mobis foram adicionados ao catalogo')

    async def adicionar_categoria(categoria, message=None):
        swfs_path = ''
        icons_path = ''
        id_pagina = get_id()
        categoria = categoria.replace("\\", "/")
        categoria_nome = categoria.split('/')[-1]
        adicionar_pagina(id_pagina, categoria_nome)
        for pasta in os.listdir(categoria):
            if pasta.lower() == 'swf' or pasta.lower() == 'swfs':
                swfs_path = os.path.abspath(os.path.join(categoria, pasta))
            if pasta.lower() == 'icon' or pasta.lower() == 'icons':
                icons_path = os.path.abspath(os.path.join(categoria, pasta))
        await adicionar_swfs(swfs_path, message)
        await adicionar_icons(icons_path, message)
        furnidata, _ids, nomes = criar_furnidatas(swfs_path, categoria_nome)##
        new_id = int(_ids[-1]) + 1
        set_id(new_id)
        await adicionar_furnidata(furnidata, message)
        await adicionar_furnitures(_ids, message=message)
        await adicionar_catalogos(id_pagina, categoria_nome, _ids, nomes=nomes, message=message)


    def adicionar_mobi(swf_path, icon_path, _id, classname, nome, descrição, id_pagina, width='1', length='1',
                       stack_heigth='0', can_stack='0', can_sit='0', is_walkable='0', sprite_id='default',
                       interaction_type='default', interaction_modes_count='10', vending_ids='0', cost_credits='0',
                       cost_diamonds='0', song_id='0', extra_data=''):
        adicionar_swf(swf_path.replace('\\', '/').replace('"', ''))
        adicionar_icon(icon_path.replace('\\', '/').replace('"', ''))
        adicionar_furnidata(criar_furnidata(_id, classname, nome, descrição))
        adicionar_furniture(_id, width=width, length=length, stack_heigth=stack_heigth, can_stack=can_stack,
                            can_sit=can_sit, is_walkable=is_walkable, sprite_id=sprite_id,
                            interaction_type=interaction_type, interaction_modes_count=interaction_modes_count,
                            vending_ids=vending_ids)
        adicionar_catalogo(id_pagina, nome, _id, cost_credits=cost_credits, cost_diamonds=cost_diamonds,
                           extradata=extra_data)

    
    async def adicionar_music_furni(nome_arquivo, nome_música, artista, song_data, message):
        musica = {
            'name[]': nome_arquivo,
            'title[]': nome_música,
            'artist[]': artista,
            'song_data[]': song_data,
            'length[]': str(song_data)[-3:]
        }
        session.post('http://setoradministrativo.agehotel.info/index.php?page=add-furniture_music', data=musica)
        await message.channel.send(f"Uma nova musica foi adicionada ao music_furni com os parametros: {nome_arquivo} {song_data}")
    
    async def hospedar_mp3(mp3, message):
        if not mp3.endswith('.mp3'):
            mp3 += '.mp3'
        with open(mp3, 'rb') as f:
            musica = {'userfile': f}
            r = session.post('http://setoradministrativo.agehotel.info/salvar_mp3.php', files=musica)
            print(r.text)
            if not 'sucesso!' in r.text:
                await message.channel.send("O arquivo é grande demais para ser hospedado :c")
                raise Exception("O arquivo é grande demais para ser hospedado :c")
            else:
                return await message.channel.send("O arquivo mp3 foi hospedado com sucesso!")

    async def adicionar_musica(mp3, song_data, nome_arquivo, nome_música, artista, song_id, _id, message):
        await hospedar_mp3(mp3, message)
        await adicionar_music_furni(nome_arquivo, nome_música, artista, song_data, message)
        await adicionar_furnidata(criar_furnidata("song_disk", nome_música, artista, _id=_id), message)
        await adicionar_furniture(_id, public_name=f"{nome_música} - {artista}" ,stack_heigth='0.1', sprite_id=_id, interaction_type='musicdisc', interaction_modes_count='2', song_id=song_id, message=message)
        await adicionar_catalogo(4206900, str(_id), f"{nome_música} - {artista}", song_id=song_id, cost_diamonds='0' ,extradata=nome_arquivo, message=message)
                

    def hospedar_gif(path):
        with open(path, 'rb') as gif:
            session.post('http://setoradministrativo.agehotel.info/salvar_emblem.php', files={'userfile[]': gif})
            print(f"{path} hospedado.")


    def hospedar_nome_emblema(codigo, nome):
        session.get(f"http://setoradministrativo.agehotel.info/index.php?page=badge_name&i%5B%5D={urllib.parse.quote(codigo)}&d%5B%5D={urllib.parse.quote(nome)}")

    
    def hospedar_desc_emblema(codigo, desc):
        session.get(f"http://setoradministrativo.agehotel.info/index.php?page=badge_desc&i%5B%5D={urllib.parse.quote(codigo)}&d%5B%5D={urllib.parse.quote(desc)}")


    def dar_emblema(nome, emblema):
        session.get(f"http://setoradministrativo.agehotel.info/index.php?page=send_emblem&i%5B%5D={nome}&ce%5B%5D={emblema}")
        return nome, emblema

    def dar_promo_points(username, points):
        data = {"player_id[]": username,
                "events[]": points
                }
        session.post(f"http://setoradministrativo.agehotel.info/index.php?page=promo_points", data=data)

    async def update_catalog_icon(catalog_id, icon_id, message=None):
        data = {"table": "catalog_pages",
                "id": str(catalog_id),
                "column": "icon_image",
                "value": str(icon_id)
                }
        await message.channel.send(f"{icon_id} foi atualizado na categoria com id {catalog_id}")
        return session.post("http://setoradministrativo.agehotel.info/update.php", data=data)

    async def update(table, id, column, value, message: discord.Message):
        data = {"table": table,
                "id": str(id),
                "column": column,
                "value": str(value)
                }
        await message.channel.send(f"Update feito na tabela {table} e coluna {column}: \n{id} valor {value}")
        return session.post("http://setoradministrativo.agehotel.info/update.php", data=data)


    def buscar_item_id_no_catalogo(item_id):
        response = session.get(f"http://setoradministrativo.agehotel.info/index.php?page=catalog_items&what=item_ids&q={item_id}")
        return response.text

    async def enviar_currency(username, moedas, diamantes, duckets):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=send_send&i={str(username)}&m={str(moedas)}&di={str(diamantes)}&du={str(duckets)}")

    def buscar_categoria_por_id(id_categoria):
        response = session.get(f"http://setoradministrativo.agehotel.info/index.php?page=catalog_pages&what=id&q={id_categoria}")
        return response.text

    def buscar_categoria_por_nome(nome_categoria):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=catalog_pages&what=caption&q={urllib.parse.quote(nome_categoria)}").text

    def buscar_sprite_id(sprite_id):
        response = session.get(f"http://setoradministrativo.agehotel.info/index.php?page=furniture&what=sprite_id&q={sprite_id}")
        return response.text


    def buscar_emblema(username, codigo):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=get_emblem&i={username}&code={codigo}").content


    def remover_emblema_por_id(_id):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=get_emblem&remover={_id}")


    def furnidata():
        response = session.get(f"https://agehotel.info/game/gamedata/ANDERSON2021.xml")
        return response.text

    def buscar_username(username, pagina="1"):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=machine&what=username&q={username}&p={str(pagina)}").text

    def buscar_ip(ip, pagina="1"):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=machine&what=ip_address&q={ip}&p={str(pagina)}").text

    def buscar_machine(machine, pagina="1"):
        return session.get(f"http://setoradministrativo.agehotel.info/index.php?page=machine&what=catalog_name&q={machine}&p={str(pagina)}").text

    def buscar_equipe():
            return session.get("https://agehotel.info/equipe.php").text.split('<div id="habbos-online">')[1]

    def buscar_amb():
            return session.get("https://agehotel.info/embaixadores.php").text.split('<div id="habbos-online">')[1]


    def check_login():
        if "ï»¿Apenas teste" in buscar_username("Steinway"):
            return login()
        else:
            return

    def check_username(username):
        requests.get(f"https://agehotel.info/home/{username}")
