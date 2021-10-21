from tinydb import TinyDB, Query

db = TinyDB('users.json')

def create_user(username: str, password: str):
    if get_user(username) is None:
        db.insert({'username': username,
                   'password': password,
                   'device_id': 123,
                   'lower_rate_limit': '',
                   'upper_rate_limit': '',
                   'atrial_amplitude': '',
                   'atrial_pw': '',
                   'ventricular_amplitude': '',
                   'ventricular_pw': '',
                   'vrp': '',
                   'arp': '',
                   'operating_mode': ''})
        return True
    return False

def get_user(username: str):
    User = Query()
    result = db.search(User.username == username)
    if (len(result)):
        return result[0]

def get_number_of_users(device_id: int):
    User = Query()
    result = db.search(User.device_id == device_id)
    return len(result)