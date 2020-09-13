import json
import logging

import requests
import telegram as tg
from telegram import ext as tg_ext

logger = logging.getLogger(__name__)

def handle_inline_query(update: tg.Update, context: tg_ext.CallbackContext):
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