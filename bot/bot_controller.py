import logging
import telegram as tg
import telegram.ext as tg_ext
from bot.bot_token_provider import BotTokenProvider
from bot.dialogs import visited_dialog

class BotController:
    def __init__(self):

        # configure logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("logger initialized. starting bot..")

        # configure telegram api
        tg_updater = tg_ext.Updater(token=BotTokenProvider.token, use_context=True)
        dispatcher = tg_updater.dispatcher

        # configure command handlers
        location_handler = tg_ext.CommandHandler('locations', self.location)
        setlocation_handler = tg.ext.CommandHandler('setlocation', self.set_location)
        howfull_handler = tg_ext.CommandHandler('wievoll', self.howfull)
        howfull_now_handler = tg_ext.CommandHandler('wievolljetzt', self.howfull_now)
        dispatcher.add_handler(location_handler)
        dispatcher.add_handler(setlocation_handler)
        dispatcher.add_handler(howfull_handler)
        dispatcher.add_handler(howfull_now_handler)
        tg_updater.start_polling()

    def location(self, update: tg.Update, context: tg_ext.CallbackContext):
        self.logger.info('"locations" called')

        from bot.gmaps.gmaps_location import GmapsLocation
        all_locations = str(GmapsLocation.location_names_as_list)
        context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


    def set_location(self, update: tg.Update, context: tg_ext.CallbackContext):
        args = context.args
        self.logger.info(f'"setlocation" called - trying to handle args: {args}')

        from bot.gmaps.user_location_mapping import UserLocationMapper
        mapper = UserLocationMapper()
        user_id = str(update.effective_user.id)

        response = mapper.set_user(user_id, args)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


    def howfull(self, update: tg.Update, context: tg_ext.CallbackContext):
        # command template: wievoll [weekday time location]
        args = context.args
        self.logger.info(f'"wievoll" called - trying to handle args: {args}')

        handler = visited_dialog.DialogHandler()

        response = handler.handle_howfull(args)
        self.logger.info('sending response...')
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


    def howfull_now(self, update: tg.Update, context: tg_ext.CallbackContext):
        args = context.args
        self.logger.info(f'"wievoll jetzt" called - trying to handle args: {args}')

        handler = visited_dialog.DialogHandler()
        user_id = str(update.effective_user.id)
        response = handler.handle_howfull_now(args, user_id)
        self.logger.info('sending response...')
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
