import re
from enum import Enum

Weekdays = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag"
]

# TODO change info to model
class HourInfo:
    """data which can be assigned to one hour"""

    def __init__(self, time: int, crowded: int, is_closed: bool = True):
        self.time = time
        self.crowded = crowded
        self.is_closed = is_closed

    def __str__(self):
        if self.is_closed:
            return f'{str(self.time)} Uhr, geschlossen'
        else:
            return f'{str(self.time)} Uhr, {str(self.crowded)} voll'


class DayInfo:
    """Encapsulates a list of HourInformation objects to represent a whole day"""

    def __init__(self, day_index: int, is_closed: bool = False):

        self.hours = [HourInfo(i, 0) for i in range(24)]
        self.day_index = day_index
        self.name = Weekdays[day_index]
        self.is_closed = is_closed

    def __str__(self):
        ret = f'{self.name}:\n'

        if self.is_closed:
            ret += 'geschlossen\n'
        else:
            for hour in self.hours:
                ret += str(hour) + '\n'
        return ret

    def set_hour(self, hour_index: int, info: HourInfo):
        self.hours[hour_index] = info

    def add_hour(self, info: HourInfo):
        self.hours.append(info)

    def get_hour(self, hour: int):
        return self.hours[hour]


class WeekInfo:
    """Encapsulates a list of DayInformation objects to represent a whole Week"""

    def __init__(self):
        self.days = [DayInfo(i) for i in range(7)]

    def __str__(self):
        ret = ''
        for day in self.days:
            ret += str(day) + '\n'
        return ret

    def set_day(self, info: DayInfo):
        self.days[info.day_index] = info

    def add_day(self, info: DayInfo):
        self.days.append(info)

    def get_day(self, weekday_index: int):
        return self.days[weekday_index]
