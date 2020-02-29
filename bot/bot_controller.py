import logging
import os
import sys

import telegram as tg
import telegram.ext as tg_ext

from bot import commands
from bot.spoiler import spoiler


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

        self.configure_command_handlers(bot_token)



    def configure_command_handlers(self, bot_token: str):
        tg_updater = tg_ext.Updater(token=bot_token, use_context=True)
        dispatcher = tg_updater.dispatcher

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

        # spoiler
        spoiler_inline_query_handler = tg_ext.InlineQueryHandler(spoiler.handle_inline_spoiler)
        dispatcher.add_handler(spoiler_inline_query_handler)

        spoiler_callback_handler = tg_ext.CallbackQueryHandler(spoiler.handle_spoiler_callback)
        dispatcher.add_handler(spoiler_callback_handler)

        dispatcher.add_error_handler(lambda update, context: self.logger.warning(context.error))
        tg_updater.start_polling()
