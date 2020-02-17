import datetime
from bot.gmaps_api import extract_raw_week, extract_current_hour, extract_raw_week_to_week_obj
from bot.weekdays import WeekInfo, HourInfo, DayInfo

# TODO: change the domain term "crowded" to "visited"
class CrowdedInfo:
    """This class provides functions for accessing how crowded a place is on google maps of a specific location"""

    weekdays = [
        'Montag',
        'Dienstag',
        'Mittwoch',
        'Donnerstag',
        'Freitag',
        'Samstag',
        'Sonntag'
    ]

    def __init__(self, location):
        maps_html = extract_raw_week(location)
        self.week: WeekInfo = extract_raw_week_to_week_obj(maps_html)
        self.current_time: HourInfo = extract_current_hour(maps_html)

    def get_crowded(self, day: str, hour: int):
        day_index: int = self.weekdays.index(day)
        day_info: DayInfo = self.week.get_day(day_index)
        hour_info: HourInfo = day_info.get_hour(hour)
        response: str = f'Am {day_info.name} zwischen {hour_info.time}:00 und {hour_info.time + 1}:00 ist ' \
                        f'es zu {hour_info.crowded}% voll. '
        return response

    def get_current_crowded(self):
        day_index: int = datetime.datetime.today().weekday()
        day_info: DayInfo = self.week.get_day(day_index)

        # get historical time info for the current situation for comparison
        statistic_hour_info: HourInfo = day_info.get_hour(self.current_time.time)
        hour_info: HourInfo = self.current_time
        response = f'Jetzt gerade ist es zu {hour_info.crowded}% voll. ' \
                   f'Normalerweise ist es am {day_info.name} zu dieser Zeit zu {statistic_hour_info.crowded}% voll.'
        return response
