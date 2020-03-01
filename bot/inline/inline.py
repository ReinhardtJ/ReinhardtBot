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
    if query.startswith('gif '):
        gif.handle_inline_gif(update, context)
    else:
        update.inline_query.answer(results=[])


def handle_inline_callback(update: tg.Update, context: tg_ext.CallbackContext):
    callback_query = update.callback_query
    if callback_query.startswith('spoiler '):
        logger.info('Handling spoiler callback')
        update.callback_query.answer(update.callback_query.data, show_alert=True)