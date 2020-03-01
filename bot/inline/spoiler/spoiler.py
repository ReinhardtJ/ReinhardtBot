import logging
import uuid

import telegram as tg
import telegram.ext as tg_ext

logger = logging.getLogger(__name__)


def handle_inline_spoiler(update: tg.Update, context: tg_ext.CallbackContext):
    query = update.inline_query.query
    results = [
        tg.InlineQueryResultArticle(
            id=uuid.uuid4(),
            title="Send",
            input_message_content=tg.InputTextMessageContent(message_text='Spoiler'),
            reply_markup=tg.InlineKeyboardMarkup(
                inline_keyboard=[[tg.InlineKeyboardButton(
                    text='Show',
                    callback_data='spoiler')]])
        )
    ]
    update.inline_query.answer(results=results)
