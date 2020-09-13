import json

import telegram as tg
from telegram import ext as tg_ext, InlineKeyboardButton, InlineKeyboardMarkup

from bot.help import logger
from bot.inline import CallbackCommands
from bot.popular_locations.data import locations


def set_location(update: tg.Update, context: tg_ext.CallbackContext):
    logger.info(f'"/setlocation" called')
    location_btns = []
    for location in locations[1:]:
        location_btns.append([InlineKeyboardButton(text=location.name, callback_data=json.dumps([CallbackCommands.SET_LOCATION, location.uid]))])

    markup = InlineKeyboardMarkup(location_btns)
    update.message.reply_text('Location auswählen', reply_markup=markup)

    # user_id = str(update.effective_user.id)
    #
    # response = set_user(user_id, args)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=response)