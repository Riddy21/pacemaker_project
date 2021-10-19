from tinydb import TinyDB, Query

db = TinyDB('users.json')

def create_user(username: str, password: str):
    if (len(get_user(username)) != 0):
        return False
    db.insert({'username': username, 'password': password})
    return True

def get_user(username: str):
    User = Query()
    result = db.search(User.username == username)
    if (len(result)):
        return result[0]