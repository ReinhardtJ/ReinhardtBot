from bot import bot_controller


def check_and_create_persistent_data():
    # TODO check for missing files and create them if necessary
    pass


def main():
    check_and_create_persistent_data()
    bot_controller.BotController()


main()
