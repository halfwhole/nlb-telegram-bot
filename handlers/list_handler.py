from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler

from db_helpers import get_all_book_info, update_availabilities
from nlb import get_availability_info


BOOKS_PREFIX = '*Books*\n'
NO_BOOKS_STRING = 'You have no books!\nUse /add to start adding new books.'
REFRESHED_NOTIFICATION = 'Refreshed!'
REFRESH_CALLBACK_DATA = 'refresh'


def lst(update, context):
    user_id = int(update.message.from_user['id'])

    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup()

    update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)


def refresh(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])

    ## Refresh availabilities
    book_info = get_all_book_info(user_id)
    ## TODO: make this async
    bids_availability_infos = [(bi['id'], get_availability_info(bi['bid'])) for bi in book_info]
    for book_id, availability_info in bids_availability_infos:
        update_availabilities(book_id, availability_info)

    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup()

    try:
        query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        ## `edit_message_text` will raise an exception if the resulting message is identical to the old one
        pass
    finally:
        query.answer(REFRESHED_NOTIFICATION)


def _get_books_text(user_id):
    book_info = get_all_book_info(user_id)
    if not book_info:
        text = NO_BOOKS_STRING
    else:
        text = BOOKS_PREFIX + '\n'.join('• %d: %s' % (bi['bid'], bi['title']) for bi in book_info)
    return text

def _get_reply_markup():
    keyboard = [[InlineKeyboardButton('Refresh', callback_data=REFRESH_CALLBACK_DATA)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


list_handler = CommandHandler('list', lst)
refresh_handler = CallbackQueryHandler(refresh, pattern='^' + REFRESH_CALLBACK_DATA + '$')
