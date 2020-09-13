class Identifiable:
    def __init__(self, uid):
        self.uid = uid


class Location(Identifiable):
    def __init__(self, name, gmaps_id, uid):
        super().__init__(uid)
        self.gmaps_id = gmaps_id
        self.name = name


class Day(Identifiable):
    def __init__(self, name, index, uid):
        super().__init__(uid)
        self.index = index
        self.name = name


class Time(Identifiable):
    def __init__(self, name, index, uid):
        super().__init__(uid)
        self.index = index
        self.name = name


class PopularityState:
    def __init__(self, location: Location = None, day: Day = None,
                 time: Time = None, next_command=None):
        self.next_command = next_command
        self.time = time
        self.day = day
        self.location = location


