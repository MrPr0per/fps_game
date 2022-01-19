from floors import load_floor

params = {}


def download_save():
    global params
    save_file = open('save0.txt').readlines()
    params = {}
    for line in save_file:
        key, value = line.strip().split('=')
        params[key] = value

    current_level_number = int(params['num_floor'])
    floor = load_floor(current_level_number)
    if not floor:
        print('')
        print('ошибка загрузки уровня')
        print('    загружен несуществующий уровень')
        print('    так что загружу двадцатый, тк он самый прикольный')
        current_level_number = 20
        floor = load_floor(current_level_number)
    return floor, current_level_number


def upload_save(params):
    save_file = open('save0.txt', 'w')
    for key, value in params.items():
        save_file.write(f'{key}={value}\n')


# upload_save({'num_floor': 18,
#              'other': 9900})
