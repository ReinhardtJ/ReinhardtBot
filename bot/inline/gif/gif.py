import json
import logging

import requests
import telegram as tg
import telegram.ext as tg_ext

from bot.api_tokens import get_tenor_token

logger = logging.getLogger(__name__)

# set the apikey and limit
apikey = get_tenor_token()

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


def handle_inline_gif(update: tg.Update, context: tg_ext.CallbackContext):
    """updates the inline query to display a list of gifs."""

    query = update.inline_query.query
    search_term = query[len('gif '):]
    logger.info(f'sending request to Tenor with {search_term}')
    response = requests.get(f'https://api.tenor.com/v1/search?key={apikey}&locale=en&tag={search_term}&limit=30')

    if response.status_code == 200:
        logger.info('results successfully retrieved.')

        gifs_dict = json.loads(response.content)
        query_answer = get_gif_list(gifs_dict)

        logger.info(f'displaying {len(query_answer)} gifs')
        update.inline_query.answer(results=query_answer, cache_time=0)
    else:
        logger.warning(f"couldn't retrieve results, http response code {response.status_code}")
        update.inline_query.answer(results=[])
