from bot import gmaps_location


def handle_user_input(args):
    if args[0] == 'jetzt':
        location: str = args[1]

        maps_location = gmaps_location.GmapsLocation(location)
        response: str = maps_location.get_current_visited()
    else:
        weekday: str = args[0]
        time = int(args[1])
        location: str = args[2]

        maps_location = gmaps_location.GmapsLocation(location)
        response = maps_location.get_visited(weekday, time)

    return response