import painel.painel
from painel.scraping import get_badges


def remover_emblema(username, codigo):
    html = painel.buscar_emblema(username, codigo)
    _id = get_badges(html)
    painel.remover_emblema_por_id(_id)
    return f"Emblema {codigo} removido do jogador {username}"
