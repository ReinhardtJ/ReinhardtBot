import logging
import traceback
import telegram as tg

from bot.gmaps import gmaps_location
from bot.gmaps import weekdays


class DialogHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.locations_urls = gmaps_location.GmapsLocation.location_urls

    def handle_howfull_now(self, args, user_id: str) -> str:
        try:
            if len(args) == 0:
                self.logger.info('no arguments for howfullnow, attempt to read from file')
                try:
                    location = self.get_location_from_userid(user_id)
                    response = self.howfull_now_from_location(location)
                except:
                    response = 'Sry ich scheinbar hast du noch keine location gesetzt. ' \
                               'Probiert mal /setlocation mit einer aus /locations.'
            elif len(args) == 1:
                location = args[0]
                response = self.howfull_now_from_location(location)

            else:
                response = "Ich brauch genau einen Parameter. Nämlich den Ort. Mach mal /locations"

            return response
        except:
            tb = traceback.format_exc()
            with open('logfile.log', 'a+', encoding='utf-8') as file:
                file.write(tb)
            self.logger.error(tb)
            return 'Es ist ein richtig heftiger Fehler aufgetreten :('

    def howfull_now_from_location(self, location: str) -> str:
        if location not in list(self.locations_urls.keys()):
            response = 'Sorry den Ort kenne ich nicht. Vielleicht kannst du ' \
                       'bald über mich selbst Orte hinzufügen! Probier mal /locations'
        else:
            maps_location = gmaps_location.GmapsLocation(location)
            response = maps_location.get_current_visited()

        return response

    def get_location_from_userid(self, user_id: str) -> str:
        self.logger.info(f'getting location from user id {user_id}')
        from bot.gmaps.user_location_mapping import UserLocationMapper
        mapper = UserLocationMapper()
        return mapper.get_location(user_id=user_id)

    def handle_howfull(self, args):
        try:
            if len(args) != 3:
                return "Ich brauch genau 3 Sachen: Einen Tag, eine Uhrzeit und einen Ort. " \
                       "zb. Dienstag 19 fitx-adenauer. Welche locations es gibt, findest " \
                       "du über /locations heraus."

            weekday = args[0]
            time = args[1]
            location = args[2]

            try:
                time = int(time)
            except ValueError:
                return f'Sorry, {time} ist leider keine Uhrzeit die ich verstehe. ' \
                       f'Wenn du Infos für z. B. 19:00 haben willst, schreib einfach "19".'

            if weekday not in weekdays.WeekModel.weekday_names:
                response = f'Sorry, den Tag "{weekday}" kenne ich nicht. Probier mal einen hiervon: ' \
                           f'{weekdays.WeekModel.weekday_names}!'
            elif time not in range(0, 24):
                response = 'Sry, die Uhrzeit muss schon >= 0 und <= 24 sein.'
            elif location not in list(self.locations_urls.keys()):
                response = 'Sorry den Ort kenne ich nicht. Vielleicht kannst du ' \
                           'bald über mich selbst Orte hinzufügen! Probier mal /locations'
            else:
                maps_location = gmaps_location.GmapsLocation(location)
                weekday_index = weekdays.WeekModel.weekday_names.index(weekday)
                response = maps_location.get_visited(weekday_index, time)
        except:
            tb = traceback.format_exc()
            with open('logfile.log', 'a+', encoding='utf-8') as file:
                file.write(tb)
            self.logger.error(tb)
            response = 'Es ist ein richtig heftiger Fehler aufgetreten :('

        return response
