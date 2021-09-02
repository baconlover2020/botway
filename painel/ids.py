import pickle

def get_id(instances=1):
    _ids = []
    with open('serialized/ids.pickle', 'rb') as load:
        currentId = pickle.load(load)
        for i in range(0, instances):
            currentId += 1
            _ids.append(currentId)
            
    with open('serialized/ids.pickle', 'wb') as dump:
        pickle.dump(int(currentId), dump)

    if len(_ids) > 1: return _ids
    return _ids[0]


def get_icon_id():
    _ids = []
    with open('serialized/icon_ids.pickle', 'rb') as load:
        currentId = pickle.load(load) + 1

    with open('serialized/icon_ids.pickle', 'wb') as dump:
        pickle.dump(int(currentId), dump)

    return currentId

if __name__ == '__main__':
    import sys
    arg = sys.argv[1]
    _id = sys.argv[2]
    if arg == 'r':
        with open('serialized/ids.pickle', 'wb') as dump:
            pickle.dump(int(_id), dump)
    if arg == 'i':
        with open('serialized/icon_ids.pickle', 'wb') as dump:
            pickle.dump(int(_id), dump)
    else: print("Use 'r' ou 'i' para ids regulares ou de icon.")

