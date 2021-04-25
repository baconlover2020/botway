import painel
from PIL import Image, ImageDraw, ImageColor
from os import remove

async def upload_gif(color1, color2=''):
    if color2=='':
        color2 = color1
    cor1 = Image.new('RGB', (40, 40), color=ImageColor.getrgb('#' + color1))
    cor2 = Image.new('RGB', (20, 40), color=ImageColor.getrgb('#' + color2))
    cores = Image.new('RGB', (40,40))
    cores.paste(cor1, (0,0))
    cores.paste(cor2,(20,0))
    cores.save(f"temp/{color1}.gif")
    return f"temp/{color1}.gif"

async def hospedar_cor(nome, color1, color2=''):
    if color2=='':
        badge_id = color1
    else:
        badge_id = f"{color1},{color2}"
    await painel.adicionar_icon(f"temp/{color1}.gif")
    await painel.adicionar_catalogo('2424000', '-1', nome, cost_diamonds='999999', extradata='name_colour', badge_id=badge_id)


