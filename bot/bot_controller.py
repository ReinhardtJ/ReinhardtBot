import logging
import traceback
import telegram.ext as tg
from bot.bot_token_provider import BotTokenProvider
from bot.visited_dialog import DialogHandler

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
main_logger = logging.getLogger(__name__)
main_logger.info("logger initialized. starting bot..")

# configure telegram api
updater = tg.Updater(token=BotTokenProvider.token, use_context=True)
dispatcher = updater.dispatcher


def location(update, context):
    main_logger.info('"locations" called')

    from bot.gmaps.gmaps_location import GmapsLocation
    all_locations = str(list(GmapsLocation.location_urls.keys()))
    context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


def visited(update, context):
    # command template: wievoll [jetzt/Wochentag Uhrzeit] [Standort]
    args = context.args
    handler = DialogHandler()
    main_logger.info('"wievoll" called - trying to handle args: ' + str(args))
    try:
        response = handler.handle_user_input(args)
        main_logger.info('successfuly retrieved workout state, sending response...')
    except:
        # with open('logfile.log', 'a+', encoding='utf-8') as file:
        #     traceback.print_exc(file=file)
        main_logger.error(traceback.format_exc())
        response = "Versteh ich nicht"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


visited_handler = tg.CommandHandler('wievoll', visited)
location_handler = tg.CommandHandler('locations', location)
dispatcher.add_handler(visited_handler)
dispatcher.add_handler(location_handler)
updater.start_polling()
