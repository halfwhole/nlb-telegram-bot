from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler

from db_helpers import get_book_info

BOOKS_PREFIX = '*Books*\n'
NO_BOOKS_STRING = 'You have no books!\nUse /add to start adding new books.'
REFRESHED_NOTIFICATION = 'Refreshed!'

## TODO: Extract duplicated parts with list_handler!!!
def refresh(update, context):
    query = update.callback_query
    ## TODO: actually write the refreshing code and call it here
    ## Refresh = db (get all book_id) >> nlb (get all availability_info) >> db (update all availabilities)
    user_id = int(query.message.chat['id'])
    book_info = get_book_info(user_id)
    if not book_info:
        text = NO_BOOKS_STRING
    else:
        text = 'MOCK REFRESHED\n' + BOOKS_PREFIX + '\n'.join('• %d: %s' % (bi['bid'], bi['title']) for bi in book_info)

    keyboard = [[InlineKeyboardButton('Refresh', callback_data='refresh')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        pass
    finally:
        query.answer(REFRESHED_NOTIFICATION)

## The `pattern` here should match `callback_data` of the list handler
refresh_handler = CallbackQueryHandler(refresh, pattern='^refresh$')
