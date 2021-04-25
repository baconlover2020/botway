from bs4 import BeautifulSoup

def verify_success(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    if not soup.find('div', {'class': 'greeting'}):
        raise Exception("Não foi possivel se conectar ao painel")
    else:
        print("Logado com sucesso")


def get_online_staffs(html):
    soup = BeautifulSoup(html, "html.parser")
    b = soup.find_all("b", attrs={"style": "color: black;"})
    staffs_on = []
    for a in b:
        staff_element = a.parent.parent.parent
        rank_element = staff_element.parent.parent.parent.parent
        staff = staff_element.find("a").text
        rank = rank_element.find("span").text
        staffs_on.append((staff, rank))
    return staffs_on

