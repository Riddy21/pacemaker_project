from tinydb import TinyDB, Query

db = TinyDB('users.json')

def create_user(username: str, password: str):
    if get_user(username) is None:
        db.insert({'username': username,
                   'password': password,
                   'device_id': 123,
                   'parameters': {
                       'lower_rate_limit': 60,
                        'upper_rate_limit': 120,
                        'atrial_amplitude': 3.5,
                        'atrial_pw': 0.4,
                        'ventricular_amplitude': 3.5,
                        'ventricular_pw': 0.4,
                        'vrp': 320,
                        'arp': 250,
                   },
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

def update_parameters(username: str, parameters: {str:str}):
    User = Query()
    u = get_user(username)
    for key in parameters:
        u['parameters'][key] = parameters[key]
    db.update({'parameters': u['parameters']}, User.username == username)
