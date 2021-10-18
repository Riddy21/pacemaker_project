from tinydb import TinyDB, Query

db = TinyDB('users.json')

def create_user(username: str, password: str):
    # check for existing user
    db.insert({'username': username, 'password': password})

def get_user(username: str):
    User = Query()
    return db.search(User.username == username)

def delete_user(username: str):
    User = Query()
    db.remove(db.remove(User.username == username))