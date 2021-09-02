import xml.etree.ElementTree as ET

class Mobi:
    def __init__(self, name, page_name):
        self.name = name
        self.page_name = page_name


search_limit = 200
exceeds_limit = "Tem mobis demais nessa busca... Tente ser mais espefico!"
not_found = "Nenhuma categoria encontrada :c"

furniture_objects_tree = ET.parse("serialized/furniture_objects.xml")
furniture_objects = furniture_objects_tree.getroot()
def buscar_mobi(key):
    key = key.lower()
    furni_list = []
    for furniture in furniture_objects:
        if key in furniture.get("name"):
            furni_list.append(Mobi(furniture.get("name"), furniture.get("page_name")))
            if len(furni_list) > search_limit:
                return exceeds_limit
    if len(furni_list) == 0:
        return not_found
    return furni_list

