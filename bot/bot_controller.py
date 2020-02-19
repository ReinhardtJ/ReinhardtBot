import logging
import traceback
from telegram.ext import Updater, CommandHandler
from bot.bot_token_provider import get_token
from bot.workout_state_dialog import handle_user_input

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
main_logger = logging.getLogger(__name__)
main_logger.info("logger initialized. starting bot..")

# configure telegram api
updater = Updater(token=get_token(), use_context=True)
dispatcher = updater.dispatcher

DEV_MODE = True

def location(update, context):
    main_logger.info('"locations" called')

    from bot.gmaps_api import location_urls
    all_locations = str(list(location_urls.keys()))
    context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


def workout_state(update, context):
    # command template: wievoll [jetzt/Wochentag Uhrzeit] [Standort]
    main_logger.info('"wievoll" called - trying to handle args: ' + str(context.args))
    try:
        response = handle_user_input(context.args)
        main_logger.info('successfuly retrieved workout state, sending response...')
    except:
        # with open('logfile.log', 'a+', encoding='utf-8') as file:
        #     traceback.print_exc(file=file)
        main_logger.error(traceback.format_exc())
        response = "Versteh ich nicht"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


workout_state_handler = CommandHandler('wievoll', workout_state)
location_handler = CommandHandler('locations', location)
dispatcher.add_handler(workout_state_handler)
dispatcher.add_handler(location_handler)
updater.start_polling()
