from painel import painel
import requests
import shutil
import os

def hospedar_emblema(url, codigo, nome, desc):
        if not url.startswith('http'):
            raise Exception("Link invalido")
        path = os.path.join('temp', f"{codigo}.gif")
        response = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
            del response
        painel.login()
        painel.hospedar_gif(path)
        painel.hospedar_nome_emblema(codigo, nome)
        painel.hospedar_desc_emblema(codigo, desc)
        os.remove(path)