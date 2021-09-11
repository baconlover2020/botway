from painel import painel
import requests
import shutil
import os
import imagehash
from PIL import Image

def hospedar_emblema(url, codigo, nome, desc):
        if not url.startswith('http'): raise UrlInvalido
        path = os.path.join('emblemas', f"{codigo}.gif")
        if os.path.isfile(path): raise EmblemaExistente
        baixar_emblema(url, path)
        painel.login()
        painel.hospedar_gif(path)
        painel.hospedar_nome_emblema(codigo, nome)
        painel.hospedar_desc_emblema(codigo, desc)


def baixar_emblema(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
        del response


def compararImagens(img1_path, img2_path,tolerancia):
    hash0 = imagehash.average_hash(Image.open(img1_path)) 
    hash1 = imagehash.average_hash(Image.open(img2_path)) 
    cutoff = 64 * tolerancia
    if hash0 - hash1 < cutoff:
        return True
    return False


def verificarDuplicados(img_path):
    img1 = os.path.join(img_path)
    _dir = 'emblemas'
    duplicados = []
    for emblema in os.listdir(_dir):
        img2= f"{_dir}/{emblema}"
        if compararImagens(img1, img2, 0.01) and img1 != img2:
            duplicados.append(emblema)
    return duplicados

def verificarDuplicadosPorUrl(url, codigo):
    path = os.path.join('temp', f"{codigo}.gif")
    baixar_emblema(url, path)
    duplicados = verificarDuplicados(path)
    os.remove(path)
    return duplicados

#errs
class UrlInvalido(Exception):
    pass

class EmblemaExistente(Exception):
    pass