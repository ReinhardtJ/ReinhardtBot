import os
from bot import bot_controller


def check_and_create_persistent_data():
    user_location_mapping_path = '../persistent_data/user_location_mapping.json'
    if not os.path.isfile(user_location_mapping_path):
        with open(user_location_mapping_path, "a+") as f:
            f.write('{}')


def main():
    check_and_create_persistent_data()
    bot_controller.BotController()


main()
