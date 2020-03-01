import logging
import sys
import os

import telegram as tg
import telegram.ext as tg_ext

from bot import commands
from bot.inline import inline
from bot.inline.spoiler import spoiler


class BotController:
    def __init__(self):

        # configure logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("logger initialized. starting bot..")

        try:
            bot_token = os.environ['BOT_TOKEN']
        except:
            self.logger.error('Bot token environment variable not set, exiting...')
            sys.exit()

        tg_updater = tg_ext.Updater(token=bot_token, use_context=True)
        dispatcher = tg_updater.dispatcher
        self.configure_command_handlers(dispatcher)
        tg_updater.start_polling()


    def configure_command_handlers(self, dispatcher: tg_ext.Dispatcher):
        # general
        help_handler = tg_ext.CommandHandler('help', commands.help)
        dispatcher.add_handler(help_handler)

        # gmaps
        location_handler = tg_ext.CommandHandler('locations', commands.location)
        dispatcher.add_handler(location_handler)

        setlocation_handler = tg.ext.CommandHandler('setlocation', commands.set_location)
        dispatcher.add_handler(setlocation_handler)

        howfull_handler = tg_ext.CommandHandler('wievoll', commands.howfull)
        dispatcher.add_handler(howfull_handler)

        howfull_now_handler = tg_ext.CommandHandler('wievolljetzt', commands.howfull_now)
        dispatcher.add_handler(howfull_now_handler)

        # inline
        inline_query_handler = tg_ext.InlineQueryHandler(inline.handle_inline_query)
        dispatcher.add_handler(inline_query_handler)

        callback_handler = tg_ext.CallbackQueryHandler(inline.handle_inline_callback)
        dispatcher.add_handler(callback_handler)
