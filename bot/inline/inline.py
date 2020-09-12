import json
import logging
import re
import uuid

import requests
import telegram as tg
from telegram import CallbackQuery, ext as tg_ext

logger = logging.getLogger(__name__)


def handle_inline_query(update: tg.Update, context: tg_ext.CallbackContext):
    query = update.inline_query.query
    if query.startswith('spoiler '):
        logger.info('Query starts with "spoiler ", handling inline spoiler..')
        handle_inline_spoiler(update, context)
    elif query.startswith('gif '):
        handle_inline_gif(update, context)
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
                    callback_data=query)]])
        )
    ]
    update.inline_query.answer(results=results)


def handle_inline_gif(update: tg.Update, context: tg_ext.CallbackContext):
    """updates the inline query to display a list of gifs."""
    from bot.api_tokens import get_tenor_token

    apikey = get_tenor_token()
    query = update.inline_query.query
    search_term = query[len('gif '):]
    logger.info(f'sending request to Tenor with {search_term}')
    response = requests.get(f'https://api.tenor.com/v1/search?key={apikey}&locale=en&tag={search_term}&limit=50')

    if response.status_code == 200:
        logger.info('results successfully retrieved.')

        gifs_dict = json.loads(response.content)
        query_answer = get_gif_list(gifs_dict)

        logger.info(f'displaying {len(query_answer)} gifs')
        update.inline_query.answer(results=query_answer, cache_time=0)
    else:
        logger.warning(f"couldn't retrieve results, http response code {response.status_code}")
        update.inline_query.answer(results=[])


def get_gif_list(gifs_dict: dict) -> list:
    gif_list = []
    results = gifs_dict['results']
    for gif in results:
        nanowebm = gif['media'][0]['nanowebm']
        truegif = gif['media'][0]['gif']
        gif_model = tg.InlineQueryResultGif(id=gif['id'],
                                            gif_url=truegif['url'],
                                            thumb_url=nanowebm['preview'],
                                            parse_mode=tg.ParseMode.HTML)
        gif_list.append(gif_model)

    return gif_list