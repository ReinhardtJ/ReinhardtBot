import logging
import uuid

from telegram import InlineQueryResultArticle, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent


class TextSpoilerHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_inline_spoiler(self, update, context):

        query = update.inline_query.query
        if str(query).startswith('spoiler '):
            results = [
                InlineQueryResultArticle(
                    id=uuid.uuid4(),
                    title="Send",
                    input_message_content=InputTextMessageContent(message_text='Spoiler'),
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[[InlineKeyboardButton(
                            text='Show',
                            callback_data=query[len('spoiler '):])]])
                )
            ]
            update.inline_query.answer(results=results)
