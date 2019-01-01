import json
import os.path
from classes import const


def save_passwords(passwords):
    try:
        with open(const.passwords, 'w') as file:
            json.dump(passwords, file)
    except Exception:
        raise Exception("Some problem with writing data.")


def load_passwords():
    try:
        with open(const.passwords, 'r') as file:
            passwords = json.load(file)
            return passwords
    except Exception:
        raise Exception("Some problem with reading data.")

def write_list_to_file(list, dest):
    if dest == "users":
        path = const.users
    else:
        path = const.file_name
    with open(path, 'w') as file:
        json.dump(list, file)


def load_json(src):
    if src == "users":
        path = const.users
    else:
        path = const.file_name
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    except Exception:
        raise Exception("Some problem with reading data.")


def save_to_json(raw_data, dest):
    if dest == "users":
        path = const.users
    else:
        path = const.file_name

    if not os.path.isfile(path):
        write_list_to_file([raw_data], dest)

    # DB is already exist and we want to add new players
    else:
        data = load_json(path)
        data.append(raw_data)
        write_list_to_file(data, dest)

