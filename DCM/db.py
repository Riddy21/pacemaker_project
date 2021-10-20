from tinydb import TinyDB, Query

db = TinyDB('users.json')

def create_user(username: str, password: str):
    if get_user(username) is None:
        db.insert({'username': username, 'password': password})
        return True
    return True

def get_user(username: str):
    User = Query()
    result = db.search(User.username == username)
    if (len(result)):
        return result[0]