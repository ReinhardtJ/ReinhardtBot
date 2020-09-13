import json
import logging
import uuid

import telegram as tg
from telegram import ext as tg_ext

logger = logging.getLogger(__name__)


def handle_callback(update: tg.Update, context: tg_ext.CallbackContext, message: str):
    logger.info('Handling spoiler callback')
    spoiler_text = message[len('spoiler '):]
    update.callback_query.answer(spoiler_text, show_alert=True)


def handle_inline_query(update: tg.Update, context: tg_ext.CallbackContext):
    from bot.inline import CallbackCommands
    query = update.inline_query.query
    results = [
        tg.InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Send",
            input_message_content=tg.InputTextMessageContent(message_text='Spoiler'),
            reply_markup=tg.InlineKeyboardMarkup(
                inline_keyboard=[[tg.InlineKeyboardButton(
                    text='Show',
                    callback_data=json.dumps([CallbackCommands.DISPLAY_SPOILER, query]))]])
        )
    ]
    update.inline_query.answer(results=results)
