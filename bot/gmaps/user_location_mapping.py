import json
import logging
import os

from bot.dialogs.popularity_dialog import location_gmaps_ids

""" The user location mapping is a dictionary which persists each user's personalized location """

rel_file_path = "../../persistent_data/user_location_mapping.json"
logger = logging.getLogger(__name__)
folder_path = os.path.dirname(os.path.abspath(__file__))
abs_file_path = os.path.join(folder_path, rel_file_path)


def read_mapping() -> dict:
    logger.info('reading json from file to dict...')
    with open(abs_file_path, 'r', encoding='utf-8') as file:
        mapping_json = json.load(file)

    logger.info(f'done reading file, retrieved dict: {mapping_json}')
    return mapping_json


def write_mapping(user_location_map: dict) -> None:
    with open(abs_file_path, 'w+', encoding='utf-8') as file:
        json.dump(user_location_map, file)
        file.truncate()


def set_user(user_id: str, args: list) -> str:
    logger.info(f'Attempting to set location for user {user_id} with args {args}...')
    if len(args) != 1:
        response = "Bitte gib mir genau eine Location aus /locations!"
    else:
        location = args[0]
        if location not in location_gmaps_ids:
            response = "Sry, diesen Ort kenne ich nicht. Versuch mal mit einem aus /locations"
        else:
            current_user_mapping: dict = read_mapping()
            current_user_mapping[user_id] = location
            write_mapping(current_user_mapping)
            response = "Location erfolgreich gespeichert!"

    return response


def get_location(user_id: str) -> str:
    logger.info(f'getting location from user id {user_id}')
    mapping_dict = read_mapping()
    logger.info(f'getting location from dict {mapping_dict}...')
    location = mapping_dict[user_id]
    logger.info(f'got location {location}')
    return mapping_dict[user_id]


