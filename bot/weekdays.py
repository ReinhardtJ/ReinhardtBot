Weekdays = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag"
]


class HourModel:
    def __init__(self, time: int, visited: int, is_closed: bool = True):
        self.time = time
        self.visited = visited
        self.is_closed = is_closed

    def __str__(self):
        if self.is_closed:
            return f'{str(self.time)} Uhr, geschlossen'
        else:
            return f'{str(self.time)} Uhr, {str(self.visited)} voll'


class DayModel:
    def __init__(self, day_index: int, is_closed: bool = False):
        self.hours = [HourModel(i, 0) for i in range(24)]  # init hours with default values
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

    def set_hour(self, hour_index: int, info: HourModel):
        self.hours[hour_index] = info

    def add_hour(self, info: HourModel):
        self.hours.append(info)

    def get_hour(self, hour: int):
        return self.hours[hour]


class WeekModel:
    """Encapsulates a list of DayInformation objects to represent a whole Week"""

    def __init__(self):
        self.days = [DayModel(i) for i in range(7)]

    def __str__(self):
        ret = ''
        for day in self.days:
            ret += str(day) + '\n'
        return ret

    def set_day(self, info: DayModel):
        self.days[info.day_index] = info

    def add_day(self, info: DayModel):
        self.days.append(info)

    def get_day(self, weekday_index: int):
        return self.days[weekday_index]
