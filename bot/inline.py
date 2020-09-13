import json
import logging
from json.decoder import JSONDecodeError

import telegram as tg
from telegram import CallbackQuery, ext as tg_ext

from bot import spoiler, gif

logger = logging.getLogger(__name__)


class CallbackCommands:
    SET_LOCATION = 'fbb92dc4'
    DISPLAY_SPOILER = '67a68cf5'

    class POPULARITY:
        SELECT_DAY = '820e3fcb'
        SELECT_TIME = 'fa91f933'
        SELECT_LOCATION = 'b57afe9d'


def handle_inline_query(update: tg.Update, context: tg_ext.CallbackContext):
    """master handler for inline queries"""
    query = update.inline_query.query
    if query.startswith('spoiler '):
        logger.info('Query starts with "spoiler ", handling inline spoiler..')
        spoiler.handle_inline_query(update, context)
    elif query.startswith('gif '):
        gif.handle_inline_query(update, context)
    else:
        logger.info('Query doesnt start with anything, removing response..')
        update.inline_query.answer(results=[])


def handle_inline_callback(update: tg.Update, context: tg_ext.CallbackContext):
    """master handler for inline callbacks"""
    query: CallbackQuery = update.callback_query
    callback_data = query.data

    try:
        parsed_data = json.loads(callback_data)
        command = parsed_data[0]
        command_data = parsed_data[1]

        if (command == CallbackCommands.POPULARITY.SELECT_LOCATION or
                command == CallbackCommands.POPULARITY.SELECT_DAY or
                command == CallbackCommands.POPULARITY.SELECT_TIME):
            from bot.popular_locations.dialog import handle_callback
            handle_callback(update, context, command=command, uid=command_data)

        elif command == CallbackCommands.SET_LOCATION:
            from bot.popular_locations.user_location_mapping import set_location_for_user
            set_location_for_user(update, context, command_data)

        elif command == CallbackCommands.DISPLAY_SPOILER:
            from bot.spoiler import handle_callback
            handle_callback(update, context, message=command_data)

    except JSONDecodeError as e:
        raise e
