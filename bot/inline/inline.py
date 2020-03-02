import logging
import uuid

import telegram as tg
import telegram.ext as tg_ext

import bot.inline.spoiler.spoiler as spoiler
import bot.inline.gif.gif as gif

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
    callback_data = update.callback_query.data
    if callback_data.startswith('spoiler '):
        logger.info('Handling spoiler callback')
        spoiler_text = callback_data[len('spoiler '):]
        update.callback_query.answer(spoiler_text, show_alert=True)
