import logging
import re

import telegram as tg
import telegram.ext as tg_ext
from telegram import CallbackQuery

import bot.inline.gif.gif as gif
import bot.inline.spoiler.spoiler as spoiler

logger = logging.getLogger(__name__)


def handle_inline_query(update: tg.Update, context: tg_ext.CallbackContext):
    query = update.inline_query.query
    if query.startswith('spoiler '):
        logger.info('Query starts with "spoiler ", handling inline spoiler..')
        spoiler.handle_inline_spoiler(update, context)
    elif query.startswith('gif '):
        gif.handle_inline_gif(update, context)
    else:
        logger.info('Query doesnt start with anything, removing response..')
        update.inline_query.answer(results=[])


def handle_inline_callback(update: tg.Update, context: tg_ext.CallbackContext):
    query: CallbackQuery = update.callback_query
    callback_data = query.data

    # check if callback_data matches a popularity callback id and forwards it to the popularity callback handler
    if (re.match(pattern='location_[0-9]{1,2}', string=callback_data) or
            re.match(pattern='day_[0-9]{1,2}', string=callback_data) or
            re.match(pattern='time_[0-9]{1,2}', string=callback_data)):
        from bot.dialogs.popularity_dialog import handle_callback
        handle_callback(update, context, query)

    if callback_data.startswith('spoiler '):
        logger.info('Handling spoiler callback')
        spoiler_text = callback_data[len('spoiler '):]
        update.callback_query.answer(spoiler_text, show_alert=True)
