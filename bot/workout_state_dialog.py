from bot.crowded import CrowdedInfo


def handle_user_input(args):
    if args[0] == 'jetzt':
        location: str = args[1]

        crowded_info: CrowdedInfo = CrowdedInfo(location)
        response: str = crowded_info.get_current_crowded()
    else:
        weekday: str = args[0]
        time = int(args[1])
        location: str = args[2]

        crowded_info = CrowdedInfo(location)
        response = crowded_info.get_crowded(weekday, time)

    return response