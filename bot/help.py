import logging
import telegram as tg
import telegram.ext as tg_ext
from telegram import ParseMode

logger = logging.getLogger(__name__)


def help(update: tg.Update, context: tg_ext.CallbackContext):
    logger.info('"/help" called')
    help_msg = """
<b>Commands</b>
<code>/help</code>
Zeige Hilfe
    
<code>/setlocation</code>
Setzt deine Standard-Location
    
<code>/wievoll</code>
Zeigt an, wie voll es am <code>WOCHENTAG</code> um <code>UHRZEIT</code> am Ort <code>LOCATION</code> ist
    
<code>/wievolljetzt</code>
Zeigt an, wie voll es jetzt gerade 
    
<b>Inline Commands</b>
<code>spoiler</code> - Versteckt die dahinterstehende Nachricht (maximal 256 Zeichen)

<code>gif</code> - Sucht eine Reihe von gifs"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg, parse_mode=ParseMode.HTML)
