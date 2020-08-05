import logging
import logging
import re
from datetime import datetime
from time import gmtime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.api_tokens import TokenNotFoundError
from bot.state.popularity_dialog_state import State, Time, Day, Location, PopularityState

logger = logging.getLogger(__name__)

# locations = [Location('FitX Gelsenkrichen Erle', 'ChIJG7JkPgXnuEcR6JH5g0AxZ68', 'location_1'], ...]
location_names = ['Mein Gym',
                  'FitX Gelsenkrichen Erle',
                  'FitX Gelsenkirchen Heßler',
                  'Sport und Gesundheitszentrum Buer',
                  'Fitnessloft Paderborn',
                  'Fit4U Paderborn',
                  'FitX Ludwigshafen']
location_gmaps_ids = ['',
                      'ChIJG7JkPgXnuEcR6JH5g0AxZ68',
                      'ChIJG7JkPgXnuEcR6JH5g0AxZ68',
                      'ChIJt-EQgGbvuEcRtaYduoWPUNE',
                      'ChIJteOG25dMukcRQtMcQscGKk8',
                      'ChIJdzSUdvZMukcRnMaZjW446Hk',
                      'ChIJs3AvWVvMl0cRb8peid0i-OE']
locations = [Location(name=location_names[i], gmaps_id=location_gmaps_ids[i], callback_id=f'location_{i}') for i in range(7)]

# days = [Day('Montag', 1, 'day_1'), ...]
day_names = ['Heute', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
days = [Day(name=day_names[i], index=i, callback_id=f'day_{i}') for i in range(8)]

# times = [Time(name='00:00', index=1, callback_id='time_1'), ...]
times = [Time(name='Jetzt', index=0, callback_id='time_0')]
for i in range(25):
    times.append(Time(name=(f'0{i}:00' if i < 10 else f'{i}:00'), index=i+1, callback_id=f'time_{i+1}'))


def send_response(query: CallbackQuery, text):
    # display message to user
    try:
        query.edit_message_text(text=text)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))
    except BadRequest as e:
        # filter out weird "Message is not modified" error
        if e.message == 'Message is not modified: specified new message content and reply markup are exactly the same ' \
                        'as a current content and reply markup of the message':
            pass
        else:
            raise e


def start_popularity_dialog(update: Update, context: CallbackContext):
    """ called when a user enters the 'howfull' command """
    chat_id = update.effective_chat.id
    State.add(chat_id, PopularityState())
    select_location(update, context)


def select_location(update: Update, context: CallbackContext):
    location_btns = []
    for location in locations:
        location_btns.append([InlineKeyboardButton(text=location.name, callback_data=location.callback_id)])

    markup = InlineKeyboardMarkup(location_btns)
    update.message.reply_text('Location auswählen', reply_markup=markup)


def select_day(update: Update, context: CallbackContext, query: CallbackQuery):
    day_btns = []
    for day in days:
        day_btns.append([InlineKeyboardButton(text=day.name, callback_data=day.callback_id)])

    markup = InlineKeyboardMarkup(day_btns)
    query.edit_message_text(text="Tag auswählen")
    query.edit_message_reply_markup(reply_markup=markup)


def select_time(update: Update, context: CallbackContext, query: CallbackQuery):
    time_btns = [[InlineKeyboardButton(text=times[0].name, callback_data=times[0].callback_id)]]
    for i in range(1, 24, 3):
        time_btns.append([
            InlineKeyboardButton(text=times[i].name, callback_data=times[i].callback_id),
            InlineKeyboardButton(text=times[i + 1].name, callback_data=times[i + 1].callback_id),
            InlineKeyboardButton(text=times[i + 2].name, callback_data=times[i + 2].callback_id)
        ])

    markup = InlineKeyboardMarkup(time_btns)
    query.edit_message_text(text='Zeit Auswählen')
    query.edit_message_reply_markup(reply_markup=markup)


def finish_popularity_dialog(update: Update, context: CallbackContext, query: CallbackQuery):
    chat_id = update.effective_chat.id
    selected_location = State.get(chat_id).location
    selected_day = State.get(chat_id).day
    selected_time = State.get(chat_id).time

    # acquire gmaps id
    gmaps_id = selected_location.gmaps_id

    # try to get the gmaps api token
    try:
        from bot.api_tokens import get_gmaps_token
        gmaps_token = get_gmaps_token()
    except TokenNotFoundError as e:
        send_response(query, e.message)
        return

    from bot.populartimes.populartimes import get_populartimes
    popularity_json = get_populartimes(gmaps_token, gmaps_id)

    # acquire day index
    if selected_day.callback_id == 'day_0':
        # user has selected 'today'
        day_index = datetime.today().weekday()
    else:
        day_index = selected_day.index

    # acquire time index
    if selected_time.callback_id == 'time_0':
        # user has selected 'now'
        try:
            popularity = popularity_json['current_popularity']
            response = f'Aktuell zu {popularity}% besucht'
        except KeyError:
            # current_time_index = int(datetime.now(datetime.timezone(datetime.timedelta(hours=1))).strftime("%H"))
            current_time_index = gmtime().tm_hour
            current_time_name = f'0{current_time_index}:00' if current_time_index < 10 else f'{current_time_index}:00'
            popularity = popularity_json['populartimes'][day_index]['data'][current_time_index]
            response = f'Leider keine Live-Daten verfügbar. Normalerweise ist es am {selected_day.name} um {current_time_name} zu {popularity}% besucht'
    else:
        popularity = popularity_json['populartimes'][day_index]['data'][selected_time.index]
        response = f'Am {selected_day.name} um {selected_time.name} zu {popularity}% besucht'

    send_response(query, response)


def handle_callback(update: Update, context: CallbackContext, query: CallbackQuery):
    chat_id = update.effective_chat.id

    if re.match(pattern='location_[0-9]{1,2}', string=query.data):
        location = [location for location in locations if location.callback_id == query.data][0]
        # check if user has a saved locations and set the gmaps id respectively or notify user to set a location
        if location.callback_id == 'location_0':
            from bot.gmaps.user_location_mapping import get_location
            try:
                user_id = update.effective_user.id
                gmaps_id = get_location(user_id)
                location.gmaps_id = gmaps_id
            except:
                # user not found in persistent data
                response = 'Du scheinst noch kein Gym ausgewählt zu haben. Bitte /setlocation benutzen. Welche Locations es gibt siehst du mit /locations'
                send_response(query, response)
                return

        State.set_values(chat_id, location=location, next_callback=select_day)
        logger.info('Handling popularity request based on location')

    if re.match(pattern='day_[0-9]{1,2}', string=query.data):
        day = [day for day in days if day.callback_id == query.data][0]
        State.set_values(chat_id, day=day, next_callback=select_time)
        logger.info('Handling popularity request based on day')

    if re.match(pattern='time_[0-9]{1,2}', string=query.data):
        time = [time for time in times if time.callback_id == query.data][0]
        State.set_values(chat_id, time=time, next_callback=finish_popularity_dialog)
        logger.info('Handling popularity request based on time - sending response')

    State.get(chat_id).next_callback(update, context, query)
