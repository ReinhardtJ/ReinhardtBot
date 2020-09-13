import json
import logging
from datetime import datetime
from time import gmtime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.api_tokens import TokenNotFoundError
from bot.popular_locations.types import Location
from bot.popular_locations.data import State, locations, days, times
from bot.inline import CallbackCommands

logger = logging.getLogger(__name__)


def send_current_popularity(update: Update, context: CallbackContext):
    """ called when a user enters the 'howfull now' command """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query

    State.add_new(chat_id, user_id)
    from bot.popular_locations.user_location_mapping import get_location
    try:
        location = get_location(user_id)
    except KeyError:
        # user not found in persistent data
        response = 'Du scheinst noch kein Gym ausgewählt zu haben.' \
                   ' Bitte /setlocation benutzen.'
        context.bot.send_message(chat_id, response)
        return
    State.set_location(chat_id, user_id, location)
    State.set_day(chat_id, user_id, days[0])
    State.set_time(chat_id, user_id, times[0])
    response = finish_popularity_dialog(update, context, query)
    context.bot.send_message(chat_id, response)


def start_popularity_dialog(update: Update, context: CallbackContext):
    """ called when a user enters the 'howfull' command """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    State.add_new(chat_id, user_id)
    select_location(update, context)


def select_location(update: Update, context: CallbackContext):
    location_btns = []
    for location in locations:
        location_btns.append([InlineKeyboardButton(text=location.name,
                                                   callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_LOCATION,
                                                                             location.uid]))])

    markup = InlineKeyboardMarkup(location_btns)
    update.message.reply_text('Location auswählen', reply_markup=markup)


def select_day(update: Update, context: CallbackContext, query: CallbackQuery):
    day_btns = []
    for day in days:
        day_btns.append([InlineKeyboardButton(text=day.name,
                                              callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_DAY,
                                                                        day.uid]))])

    markup = InlineKeyboardMarkup(day_btns)
    query.edit_message_text(text="Tag auswählen")
    query.edit_message_reply_markup(reply_markup=markup)


def select_time(update: Update, context: CallbackContext, query: CallbackQuery):
    time_btns = [[InlineKeyboardButton(text=times[0].name,
                                       callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_TIME,
                                                                 times[0].uid]))]]
    for i in range(1, 24, 3):
        time_btns.append([
            InlineKeyboardButton(text=times[i].name,
                                 callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_TIME, times[i].uid])),
            InlineKeyboardButton(text=times[i + 1].name,
                                 callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_TIME, times[i + 1].uid])),
            InlineKeyboardButton(text=times[i + 2].name,
                                 callback_data=json.dumps([CallbackCommands.POPULARITY.SELECT_TIME, times[i + 2].uid]))
        ])

    markup = InlineKeyboardMarkup(time_btns)
    query.edit_message_text(text='Zeit Auswählen')
    query.edit_message_reply_markup(reply_markup=markup)


def finish_popularity_dialog(update: Update, context: CallbackContext, query: CallbackQuery) -> str:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    selected_location = State.get(chat_id, user_id).location
    selected_day = State.get(chat_id, user_id).day
    selected_time = State.get(chat_id, user_id).time

    # acquire popular_locations id
    gmaps_id = selected_location.gmaps_id

    # try to get the popular_locations api token
    try:
        from bot.api_tokens import get_gmaps_token
        gmaps_token = get_gmaps_token()
    except TokenNotFoundError as e:
        send_response(query, e.message)
        return

    from bot.popular_locations.populartimes import get_populartimes
    popularity_json = get_populartimes(gmaps_token, gmaps_id)

    # acquire day index
    if selected_day.index == 0:
        # user has selected 'today'
        day_index = datetime.today().weekday()
    else:
        day_index = selected_day.index

    # acquire time index
    if selected_time.index == 0:
        # user has selected 'now'
        try:
            popularity = popularity_json['current_popularity']
            response = f'Aktuell im {selected_location.name} zu {popularity}% besucht'
        except KeyError:
            # current_time_index = int(datetime.now(datetime.timezone(datetime.timedelta(hours=1))).strftime("%H"))
            current_time_index = gmtime().tm_hour
            current_time_name = f'0{current_time_index}:00' if current_time_index < 10 else f'{current_time_index}:00'
            popularity = popularity_json['populartimes'][day_index]['data'][current_time_index]
            response = f'Leider keine Live-Daten verfügbar. Normalerweise ist es am {selected_day.name} um {current_time_name} zu {popularity}% besucht!'
    else:
        popularity = popularity_json['populartimes'][day_index]['data'][selected_time.index]
        if selected_day.index == 0:
            response = f'Heute um {selected_time.name} im {selected_location.name} zu {popularity}% besucht!'
        else:
            response = f'Am {selected_day.name} um {selected_time.name} im {selected_location.name} zu {popularity}% besucht!'

    return response


def handle_callback(update: Update, context: CallbackContext, command: str, uid: str):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    query = update.callback_query

    if command == CallbackCommands.POPULARITY.SELECT_LOCATION:
        location: Location = next(filter(lambda l: l.uid == uid, locations))
        if location.uid == '68cc82b1':
            try:
                from bot.popular_locations.user_location_mapping import get_location
                location = get_location(user_id)
            except KeyError:
                # user not found in persistent data
                response = 'Du scheinst noch kein Gym ausgewählt zu haben.' \
                           ' Bitte /setlocation benutzen.'
                send_response(update.callback_query, response)
                return

        State.set_location(chat_id, user_id, location)
        State.set_next_command(chat_id, user_id, CallbackCommands.POPULARITY.SELECT_DAY)
        logger.info('Handling popularity request based on location')
        select_day(update, context, query)

    if command == CallbackCommands.POPULARITY.SELECT_DAY:
        day = next(filter(lambda d: d.uid == uid, days))
        State.set_day(chat_id, user_id, day)
        logger.info('Handling popularity request based on day')
        select_time(update, context, query)

    if command == CallbackCommands.POPULARITY.SELECT_TIME:
        time = next(filter(lambda t: t.uid == uid, times))
        State.set_time(chat_id, user_id, time)
        logger.info('Handling popularity request based on time - sending response')
        response = finish_popularity_dialog(update, context, query)
        send_response(query, response)


def send_response(query: CallbackQuery, text):
    # display message to user
    try:
        query.edit_message_text(text=text)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))
    except BadRequest as e:
        # filter out weird "Message is not modified" error
        if 'Message is not modified' in e.message:
            pass
        else:
            raise e
