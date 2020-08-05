import logging
import os

logger = logging.getLogger(__name__)


class TokenNotFoundError(RuntimeError):
    def __init__(self, message):
        self.message = message


def get_gmaps_token():
    try:
        api_key = os.environ['GMAPS_API_TOKEN']
        return api_key
    except:
        msg = 'Gmaps api token environment variable not set'
        logger.error(msg)
        raise TokenNotFoundError(msg)


def get_bot_token():
    try:
        bot_token = os.environ['BOT_TOKEN']
        return bot_token
    except:
        msg = 'Bot token environment variable not set'
        logger.error(msg)
        raise TokenNotFoundError(msg)


def get_tenor_token():
    try:
        tenor_token = os.environ['TENOR_API_KEY']
        return tenor_token
    except:
        msg = 'Tenor API Token environment variable not set'
        logger.error(msg)
        raise TokenNotFoundError(msg)