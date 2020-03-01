import logging
import telegram as tg
import telegram.ext as tg_ext
from telegram import ParseMode

from bot.dialogs import visited_dialog
from bot.gmaps import user_location_mapping, gmaps_location


logger = logging.getLogger(__name__)

def help(update: tg.Update, context: tg_ext.CallbackContext):
    logger.info('"/help" called')
    help_msg = """
<b>Commands</b>
<code>/help</code>
Zeige Hilfe
    
<code>/locations</code>
Zeigt alle im Bot gespeicherten Google Maps Orte
    
<code>/setlocation LOCATION</code>
Setzt deinen Standardort auf <code>LOCATION</code>
    
<code>/wievoll WOCHENTAG UHRZEIT LOCATION</code>
Zeigt an, wie voll es am <code>WOCHENTAG</code> um <code>UHRZEIT</code> am Ort <code>LOCATION</code> ist

    <code>WOCHENTAG  </code>z.B. Montag, Dienstag, ...
    <code>UHRZEIT    </code>z.B. 0, 1, 22 (entspricht 0:00, 01:00, 22:00)
    <code>LOCATION   </code>Siehe <code>/location</code>, um alle erlaubten Orte zu sehen
    
    
<code>/wievolljetzt LOCATION</code>
Zeigt an, wie voll es jetzt gerade am Ort <code>LOCATION</code> ist. Wenn per <code>/setlocation</code> ein Ort gesetzt wurde, ist der Parameter optional
    
<b>Inline Commands</b>
<code>spoiler</code> - Versteckt die dahinterstehende Nachricht (maximal 256 Zeichen)

<code>gif</code> - Sucht eine Reihe von gifs"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg, parse_mode=ParseMode.HTML)

def location(update: tg.Update, context: tg_ext.CallbackContext):
    logger.info('"/locations" called')

    all_locations = str(gmaps_location.GmapsLocation.location_names_as_list)
    context.bot.send_message(chat_id=update.effective_chat.id, text=all_locations)


def set_location(update: tg.Update, context: tg_ext.CallbackContext):
    args = context.args
    logger.info(f'"/setlocation" called - trying to handle args: {args}')

    mapper = user_location_mapping.UserLocationMapper()
    user_id = str(update.effective_user.id)

    response = mapper.set_user(user_id, args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def howfull(update: tg.Update, context: tg_ext.CallbackContext):
    # command template: wievoll [weekday time location]
    args = context.args
    logger.info(f'"/wievoll" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()

    response = handler.handle_howfull(args)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def howfull_now(update: tg.Update, context: tg_ext.CallbackContext):
    args = context.args
    logger.info(f'"/wievoll jetzt" called - trying to handle args: {args}')

    handler = visited_dialog.DialogHandler()
    user_id = str(update.effective_user.id)
    response = handler.handle_howfull_now(args, user_id)
    logger.info('sending response...')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
