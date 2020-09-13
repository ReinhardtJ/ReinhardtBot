import json
import logging
import os
import telegram as tg
from telegram import InlineKeyboardMarkup, ext as tg_ext
from telegram.error import BadRequest

from bot.popular_locations.data import locations
from bot.popular_locations.types import Location

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


def set_location_for_user(update: tg.Update, context: tg_ext.CallbackContext, location_uid: str):
    user_id = update.effective_user.id
    query = update.callback_query
    logger.info(f'Attempting to set location for user {user_id}...')
    try:
        current_user_mapping: dict = read_mapping()
        current_user_mapping[user_id] = location_uid
        write_mapping(current_user_mapping)
        response = "Location erfolgreich gespeichert!"
    except:
        response = "Location konnte nicht gespeichert werden :("

    try:
        query.edit_message_text(response)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))
    except BadRequest as e:
        if 'Message is not modified' in e.message:
            pass
        else:
            raise e


def get_location(user_id: str) -> Location:
    logger.info(f'getting location from user id {user_id}')
    mapping_dict = read_mapping()
    logger.info(f'getting location from dict {mapping_dict}...')
    location_uid = mapping_dict[str(user_id)]
    logger.info(f'got location {location_uid}')
    return next(filter(lambda l: l.uid == location_uid, locations))
