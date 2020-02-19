from bot.gmaps_api import MapsLocation


def handle_user_input(args):
    if args[0] == 'jetzt':
        location: str = args[1]

        visited_model: MapsLocation = MapsLocation(location)
        response: str = visited_model.get_current_visited()
    else:
        weekday: str = args[0]
        time = int(args[1])
        location: str = args[2]

        visited_model = MapsLocation(location)
        response = visited_model.get_visited(weekday, time)

    return response