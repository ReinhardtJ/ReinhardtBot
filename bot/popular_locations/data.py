from bot.popular_locations.types import PopularityState, Location, Day, Time


class State:
    """simple static state object to collect user input """
    entries = {}

    @staticmethod
    def add_new(chat_id: str, user_id: str):
        State.entries[f'{chat_id}{user_id}'] = PopularityState()

    @staticmethod
    def set_location(chat_id: str, user_id: str, location: Location):
        State.entries[f'{chat_id}{user_id}'].location = location

    @staticmethod
    def set_day(chat_id: str, user_id: str, day: Day):
        State.entries[f'{chat_id}{user_id}'].day = day

    @staticmethod
    def set_time(chat_id: str, user_id: str, time: Time):
        State.entries[f'{chat_id}{user_id}'].time = time

    @staticmethod
    def set_next_command(chat_id: str, user_id: str, command: str):
        State.entries[f'{chat_id}{user_id}'].next_command = command

    @staticmethod
    def get(chat_id: str, user_id: str) -> PopularityState:
        return State.entries[f'{chat_id}{user_id}']

    @staticmethod
    def delete(chat_id: str, user_id: str):
        del State.entries[f'{chat_id}{user_id}']


locations = [
    Location(name='Mein Gym', gmaps_id='', uid='68cc82b1'),
    Location(name='FitX Gelsenkrichen Erle', gmaps_id='ChIJG7JkPgXnuEcR6JH5g0AxZ68', uid='b51aaaad'),
    Location(name='FitX Gelsenkirchen Heßler', gmaps_id='ChIJG7JkPgXnuEcR6JH5g0AxZ68', uid='74058616'),
    Location(name='Sport und Gesundheitszentrum Buer', gmaps_id='ChIJt-EQgGbvuEcRtaYduoWPUNE', uid='4ca10842'),
    Location(name='Fitnessloft Paderborn', gmaps_id='ChIJteOG25dMukcRQtMcQscGKk8', uid='f0d7d3ec'),
    Location(name='Fit4U Paderborn', gmaps_id='ChIJdzSUdvZMukcRnMaZjW446Hk', uid='9da2b2f6'),
    Location(name='FitX Ludwigshafen', gmaps_id='ChIJs3AvWVvMl0cRb8peid0i', uid='7deacfde'),
]
days = [
    Day(name='Heute', index=0, uid='72d5d2c4'),
    Day(name='Montag', index=1, uid='b1690669'),
    Day(name='Dienstag', index=2, uid='f3952e57'),
    Day(name='Mittwoch', index=3, uid='3c0727c2'),
    Day(name='Donnerstag', index=4, uid='095c0754'),
    Day(name='Freitag', index=5, uid='7c337ae4'),
    Day(name='Samstag', index=6, uid='b9c696f6'),
    Day(name='Sonntag', index=7, uid='e2bc1278')
]
times = [
    Time(name='Jetzt', index=0, uid='9a3dd671'),
    Time(name='01:00', index=1, uid='670e92d4'), Time(name='02:00', index=2, uid='39e601da'),
    Time(name='03:00', index=3, uid='f10a21f1'), Time(name='04:00', index=4, uid='6625a38a'),
    Time(name='05:00', index=5, uid='f234984b'), Time(name='06:00', index=6, uid='4a068a09'),
    Time(name='07:00', index=7, uid='011553c8'), Time(name='08:00', index=8, uid='e559cf7c'),
    Time(name='09:00', index=9, uid='f004a7a8'), Time(name='10:00', index=10, uid='c4509891'),
    Time(name='11:00', index=11, uid='5fa700c4'), Time(name='12:00', index=12, uid='66a9c428'),
    Time(name='13:00', index=13, uid='3b509808'), Time(name='14:00', index=14, uid='12f25bc2'),
    Time(name='15:00', index=15, uid='edda5915'), Time(name='16:00', index=16, uid='2c6af257'),
    Time(name='17:00', index=17, uid='83817931'), Time(name='18:00', index=18, uid='04597697'),
    Time(name='19:00', index=19, uid='a37ccb55'), Time(name='20:00', index=20, uid='56c6b4e9'),
    Time(name='21:00', index=21, uid='20dc28ae'), Time(name='22:00', index=22, uid='d0ebedb4'),
    Time(name='23:00', index=23, uid='14116833'), Time(name='00:00', index=25, uid='ddc5cd92'),
]