from . import painel
from .ids import get_id
import os

def adicionar_categoria(categoria):
        swfs_path = ''
        icons_path = ''
        id_pagina = get_id()
        categoria = categoria.replace("\\", "/")
        categoria_nome = categoria.split('/')[-1]
        painel.login()
        painel.adicionar_pagina(id_pagina, categoria_nome)
        for pasta in os.listdir(categoria):
            if pasta.lower().startswith('swf'):
                swfs_path = os.path.abspath(os.path.join(categoria, pasta))
            if pasta.lower().startswith('icon'):
                icons_path = os.path.abspath(os.path.join(categoria, pasta))
        swfsAdicionadas = adicionar_swfs(swfs_path)
        iconsAdicionados = adicionar_icons(icons_path)
        furnidata, _ids, nomes = criar_furnidatas(swfs_path, categoria_nome)##
        painel.adicionar_furnidata(furnidata)
        furnituresAdicionados = adicionar_furnitures(_ids, nomes=nomes)
        catalogosAdicionados = adicionar_catalogos(id_pagina, categoria_nome, _ids, nomes=nomes)
        return swfsAdicionadas + iconsAdicionados + furnituresAdicionados +catalogosAdicionados, furnidata



def adicionar_swfs(swfs_path):
        print('---------- Hospedando SWFS ----------')
        log = '---------- SWFS ----------\n'
        for swf in os.listdir(swfs_path):
            swfLog =  painel.adicionar_swf(os.path.join(swfs_path, swf))
            log += f"O SWF {swfLog} foi hospedado com sucesso.\n"
        print('Todas SWFs da pasta foram hospedada')
        return log


def adicionar_icons(icons_path):
        icons_path = icons_path.replace('\\', '/').replace('"', '')
        print('---------- Hospedando Icones ----------')
        log = '---------- Icons ----------\n'
        for icon in os.listdir(icons_path):
            iconLog = painel.adicionar_icon(os.path.join(icons_path, icon))
            log += f"O icon {iconLog} foi hospedado com sucesso.\n"
        print("Todos os icones foram hospedados.")
        return log



def criar_furnidatas(swf_path, categoria):
        print(f'---------- Criando furnidata para {categoria} ----------')
        furnidata = ''
        nomes = {}
        _ids = []
        for swf in os.listdir(swf_path):
            _id = get_id()
            nome = criar_nome(swf)
            furnidata += painel.criar_furnidata(swf.replace('.swf', ''), nome, categoria, _id=_id)
            _ids.append(_id)
            nomes[_id] = nome
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


def adicionar_furnitures(_ids, public_name='steinlindo', item_name='steinlindo', _type='s', width='1', length='1',
                        stack_heigth='0', can_stack='1', can_sit='0', is_walkable='0',
                        sprite_id='', allow_gift='1', interaction_type='default', interaction_modes_count='10', vending_ids='0',
                        effect_id='0', variable_heights='0', song_id='0', nomes=None):
    log = '---------- Furnitures (DB) ----------\n'
    for _id in _ids:
        logFurni = painel.adicionar_furniture(_id, public_name=nomes[_id], item_name=nomes[_id], _type=_type, width=width, length=length,
                        stack_heigth=stack_heigth, can_stack=can_stack, can_sit=can_sit, is_walkable=is_walkable,
                        sprite_id=sprite_id, allow_gift='0', interaction_type=interaction_type, interaction_modes_count=interaction_modes_count, vending_ids=vending_ids,
                        effect_id=effect_id, variable_heights=variable_heights, song_id=song_id)
        log += f'Furniture adicionado : {logFurni}\n'
    print('Todos os mobis foram adicionados ao furniture')
    return log


def adicionar_catalogos(id_pagina, nome_pagina, _ids, cost_credits='5', cost_diamonds='9999999', nomes=None ):
        log = '---------- Catalogo ----------\n'
        for _id in _ids:
            logCatalogo = painel.adicionar_catalogo(id_pagina, _id, nomes[_id], cost_credits, cost_diamonds=cost_diamonds)
            log += f"Catalogo adicionado: {logCatalogo}\n"
        print('Todos os mobis foram adicionados ao catalogo')
        return log