import logging
import telegram as tg
import telegram.ext as tg_ext
from bot.bot_token_provider import BotTokenProvider
from bot import visited_dialog

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("logger initialized. starting bot..")

# configure telegram api
updater = tg_ext.Updater(token=BotTokenProvider.token, use_context=True)
dispatcher = updater.dispatcher


def location(update: tg.Update, context: tg_ext.CallbackContext):
    logger.info('"locations" called')

    from bot.gmaps.gmaps_location import GmapsLocation
    all_locations = str(GmapsLocation.location_names_as_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


def set_location(update: tg.Update, context: tg_ext.CallbackContext):
    args = context.args
    logger.info(f'"setlocation" called - trying to handle args: {args}')

    from bot.gmaps.user_location_mapping import UserLocationMapper
    mapper = UserLocationMapper()
    user_id = str(update.effective_user.id)

    response = mapper.set_user(user_id, args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def howfull(update: tg.Update, context: tg_ext.CallbackContext):
    # command template: wievoll [weekday time location]
    args = context.args
    logger.info(f'"wievoll" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()

    response = handler.handle_howfull(args)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def howfull_now(update: tg.Update, context: tg_ext.CallbackContext):
    # command template: wievoll jetzt [location]
    args = context.args
    logger.info(f'"wievoll jetzt" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()
    user_id = str(update.effective_user.id)
    response = handler.handle_howfull_now(args, user_id)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


location_handler = tg_ext.CommandHandler('locations', location)
setlocation_handler = tg.ext.CommandHandler('setlocation', set_location)
howfull_handler = tg_ext.CommandHandler('wievoll', howfull)
howfull_now_handler = tg_ext.CommandHandler('wievolljetzt', howfull_now)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(setlocation_handler)
dispatcher.add_handler(howfull_handler)
dispatcher.add_handler(howfull_now_handler)
updater.start_polling()
