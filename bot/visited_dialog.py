from bot.gmaps import gmaps_location


class DialogHandler:
    def __init__(self):
        self.locations_urls = gmaps_location.GmapsLocation.location_urls

    def handle_user_input(self, args):
        if args[0] == 'jetzt':
            location: str = args[1]

            if location not in list(self.locations_urls.keys()):
                response = 'Sorry den Ort kenne ich nicht. Vielleicht kannst du ' \
                           'bald über mich selbst Orte hinzufügen!'
            else:
                maps_location = gmaps_location.GmapsLocation(location)
                response: str = maps_location.get_current_visited()
        else:
            weekday: str = args[0]
            time = int(args[1])
            location: str = args[2]

            maps_location = gmaps_location.GmapsLocation(location)
            response = maps_location.get_visited(weekday, time)

        return response
