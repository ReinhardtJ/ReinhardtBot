import logging
import uuid

import telegram as tg
import telegram.ext as tg_ext

logger = logging.getLogger(__name__)

def handle_inline_spoiler(update: tg.Update, context: tg_ext.CallbackContext):

    query = update.inline_query.query
    if str(query).startswith('spoiler '):
        results = [
            tg.InlineQueryResultArticle(
                id=uuid.uuid4(),
                title="Send",
                input_message_content=tg.InputTextMessageContent(message_text='Spoiler'),
                reply_markup=tg.InlineKeyboardMarkup(
                    inline_keyboard=[[tg.InlineKeyboardButton(
                        text='Show',
                        callback_data=query[len('spoiler '):])]])
            )
        ]
        update.inline_query.answer(results=results)
    else:
        update.inline_query.answer(results=[])


def handle_spoiler_callback(update: tg.Update, context: tg_ext.CallbackContext):
    update.callback_query.answer(update.callback_query.data, show_alert=True)
