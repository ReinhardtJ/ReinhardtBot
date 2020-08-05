import os
from bot import bot_controller


# check and create persistent data file if it doesnt exist
user_location_mapping_path = '../persistent_data'
filename = 'user_location_mapping.json'
user_location_mapping_filepath = os.path.join(user_location_mapping_path, filename)
if not os.path.isdir(user_location_mapping_path):
    os.mkdir(user_location_mapping_path, mode=0o777)
if not os.path.isfile(user_location_mapping_filepath):
    with open(user_location_mapping_filepath, "a+") as f:
        f.write('{}')

bot_controller.start()
