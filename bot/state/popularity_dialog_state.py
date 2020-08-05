class Location:
    def __init__(self, name, gmaps_id, callback_id):
        self.callback_id = callback_id
        self.gmaps_id = gmaps_id
        self.name = name


class Day:
    def __init__(self, name, index, callback_id):
        self.callback_id = callback_id
        self.index = index
        self.name = name


class Time:
    def __init__(self, name, index, callback_id):
        self.callback_id = callback_id
        self.index = index
        self.name = name


class PopularityState:
    def __init__(self, location: Location = None, day: Day = None, time: Time = None, next_callback=None):
        self.next_callback = next_callback
        self.time = time
        self.day = day
        self.location = location


class State:
    """simple static state object to collect user input """
    entries = {}

    @staticmethod
    def add(id: str, popularity: PopularityState):
        State.entries[id] = popularity

    @staticmethod
    def set_values(id: str, location: Location = None, day: Day = None, time: Time = None, next_callback=None):
        if location:
            State.entries[id].location = location
        if day:
            State.entries[id].day = day
        if time:
            State.entries[id].time = time
        if next_callback:
            State.entries[id].next_callback = next_callback

    @staticmethod
    def get(id: str) -> PopularityState:
        return State.entries[id]

    @staticmethod
    def delete(id: str):
        del State.entries[id]
