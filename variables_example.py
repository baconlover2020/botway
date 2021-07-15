import pickle

class Auth:
    def __init__(self, username, password, pin, security_link):
        self.username = username
        self.password = password
        self.payload = {'i': self.username, 'd': self.password}
        self.pin = {'pin': pin}
        self.security_link = security_link


class User:
    def __init__(self, name, _id, can_add_furni=False, can_add_badge=False, is_admin=False):
        self.name = name
        self.id = _id
        self.can_add_furni = can_add_furni
        self.can_add_badge = can_add_badge
        self.is_admin = is_admin


def get_user_list():
    with open('vars/users', 'rb') as f:
        return pickle.load(f)


def set_users(a):
    with open('vars/users', 'wb') as f:
        pickle.dump(a, f)


def get_id():
    with open('vars/furni_ids', 'rb') as f:
     furni_id, icon_id = pickle.load(f)
     furni_id += 1
     with open('vars/furni_ids', 'wb') as w:
        pickle.dump([furni_id, icon_id], w)
     return str(furni_id)

def set_id(_id):
    with open('vars/furni_ids', 'rb') as f:
     furni_id, icon_id = pickle.load(f)
     with open('vars/furni_ids', 'wb') as w:
        pickle.dump([_id, icon_id], w)
     

def get_icon_id():
    with open('vars/furni_ids', 'rb') as f:
     furni_id, icon_id = pickle.load(f)
     icon_id += 1
     with open('vars/furni_ids', 'wb') as w:
        pickle.dump([furni_id, icon_id], w)
     return str(icon_id)



auth = Auth(
    username= 'Martinhamiguelangelo9',
    password= 'martinha123',
    pin = '154236',
    security_link= 'http://setoradministrativo.agehotel.info/login.php?securitysystem=AndersonAge'
    )

channels = [
    290363547769372672,
    837803727485534218,
    834895207069122580,
    ]
bot_token = 'ODM4OTMwNTQ1NDg3NTExNTYz.YJCQ9A.4s-d4lMa6LPw5jXg7q1Z3Qnn4qg'

user_list = get_user_list()
users = [User(name, _id, can_add_furni, can_add_badge, is_admin) for name, _id, can_add_furni, can_add_badge, is_admin in user_list]






#a = [['steinway', 226546766940471296, True, True, True], ['teresa170', 403362226632917015, True, True, True], ['glaciara', 692427544108073020, True, True, False], ['lolaindaeyo', 577606805081948170, True, True, False]]
#set_users(a)