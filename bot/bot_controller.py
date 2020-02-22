import logging
import telegram.ext as tg
from bot.bot_token_provider import BotTokenProvider
from bot import visited_dialog

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("logger initialized. starting bot..")

# configure telegram api
updater = tg.Updater(token=BotTokenProvider.token, use_context=True)
dispatcher = updater.dispatcher


def location(update, context):
    logger.info('"locations" called')

    from bot.gmaps.gmaps_location import GmapsLocation
    all_locations = str(list(GmapsLocation.location_urls.keys()))
    context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


def howfull(update, context):
    # command template: wievoll [weekday time location]
    args = context.args
    logger.info(f'"wievoll" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()

    response = handler.handle_howfull(args)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def howfull_now(update, context):
    # command template: wievoll jetzt [location]
    args = context.args
    logger.info(f'"wievoll jetzt" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()
    response = handler.handle_howfull_now(args)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


location_handler = tg.CommandHandler('locations', location)
howfull_handler = tg.CommandHandler('wievoll', howfull)
howfull_now_handler = tg.CommandHandler('wievolljetzt', howfull_now)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(howfull_handler)
dispatcher.add_handler(howfull_now_handler)
updater.start_polling()
