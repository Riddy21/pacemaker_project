from tinydb import TinyDB, Query

db = TinyDB('users.json')
UserQuery = Query()

def create_user(username: str, password: str):
    if get_user(username) is None:
        db.insert({'username': username,
                   'password': password,
                   'device_id': 123,
                   'parameters': {
                       'lower_rate_limit': 60,
                        'upper_rate_limit': 120,
                        'max_sensor_rate': 120,
                        'fixed_av_delay': 150,
                        'atrial_amplitude': 5,
                        'atrial_pw': 1,
                        'atrial_sensitivity': '',
                        'ventricular_amplitude': 5,
                        'ventricular_pw': 1,
                        'ventricular_sensitivity': '',
                        'vrp': 320,
                        'arp': 250,
                        'pvarp': 250,
                        'hysteresis': 0,
                        'rate_smoothing': 0,
                        'activity_threshold': 'Med',
                        'reaction_time': 30,
                        'response_factor': 8,
                        'recovery_time': 5
                   },
                   'operating_mode': ''})
        return True
    return False

def get_user(username: str):
    result = db.search(UserQuery.username == username)
    if (len(result)):
        return result[0]

def get_number_of_users(device_id: int):
    result = db.search(UserQuery.device_id == device_id)
    return len(result)

def update_parameters(username: str, parameters):
    user = get_user(username)
    for key in parameters:
        #user['parameters'][key] = parameters[key].get()
        user['parameters'][key] = parameters[key]
    db.update({'parameters': user['parameters']}, UserQuery.username == username)

def update_operating_mode(username: str, mode: str):
    db.update({'operating_mode': mode}, UserQuery.username == username)
