from bot.visited import VisitedModel


def handle_user_input(args):
    if args[0] == 'jetzt':
        location: str = args[1]

        visited_model: VisitedModel = VisitedModel(location)
        response: str = visited_model.get_current_visited()
    else:
        weekday: str = args[0]
        time = int(args[1])
        location: str = args[2]

        visited_model = VisitedModel(location)
        response = visited_model.get_visited(weekday, time)

    return response