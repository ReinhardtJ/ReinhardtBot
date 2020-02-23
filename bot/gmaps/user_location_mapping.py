import json
import os
import bot.gmaps.gmaps_location as gmaps_location
import logging

class UserLocationMapper:
    rel_file_path = "user_location_mapping.json"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        folder_path = os.path.dirname(os.path.abspath(__file__))
        self.abs_file_path = os.path.join(folder_path, UserLocationMapper.rel_file_path)

    def get_location(self, user_id: str) -> str:
        self.logger.info(f'getting location from user id {user_id}')
        mapping_dict = self.read_json_file_to_dict()
        self.logger.info(f'getting location from dict {mapping_dict}...')
        location = mapping_dict[user_id]
        self.logger.info(f'got location {location}')
        return mapping_dict[user_id]

    def set_user(self, user_id: str, args: list) -> str:
        self.logger.info(f'Attempting to set location for user {user_id} with args {args}...')
        if len(args) != 1:
            response = "Bitte gib mir genau eine Location aus /locations!"
        else:
            location = args[0]
            if location not in gmaps_location.GmapsLocation.location_names_as_list:
                response = "Sry, diesen Ort kenne ich nicht. Versuch mal mit einem aus /locations"
            else:
                current_user_mapping: dict = self.read_json_file_to_dict()
                current_user_mapping[user_id] = location
                self.write_dict_to_json_file(current_user_mapping)
                response = "Location erfolgreich gespeichert!"

        return response

    def write_dict_to_json_file(self, user_location_map: dict) -> None:
        with open(self.abs_file_path, 'w+', encoding='utf-8') as file:
            json.dump(user_location_map, file)
            file.truncate()

    def read_json_file_to_dict(self) -> dict:
        self.logger.info('reading json from file to dict...')
        with open(self.abs_file_path, 'r', encoding='utf-8') as file:
            mapping_json = json.load(file)

        self.logger.info(f'done reading file, retrieved dict: {mapping_json}')
        return mapping_json

# mapper = UserLocationMapper()
# print(mapper.get_location("298077132"))