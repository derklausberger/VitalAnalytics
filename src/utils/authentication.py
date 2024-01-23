import json
import os

USER_DATA_FILE_PATH = os.path.join(os.getcwd(), "utils", "userdata.json")


def load_user_data():
    if os.path.exists(USER_DATA_FILE_PATH):
        with open(USER_DATA_FILE_PATH, "r") as file:
            user_data = json.load(file)
        return user_data
    else:
        return {}


def save_user_data(user_data):
    with open(USER_DATA_FILE_PATH, "w") as file:
        json.dump(user_data, file)


def check_login(user_data, password):
    user_dict = load_user_data()
    saved_password = user_dict.get(user_data)

    print(user_dict)

    if saved_password is not None and saved_password == password:
        return True
    else:
        return False
