from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler

from db_helpers import get_all_book_info, refresh_all_availabilities

BOOKS_PREFIX = '<b>Books:</b> across all libraries\n'
NO_BOOKS_STRING = 'You have no books!\nUse /add to start adding new books.'
REPLY_MARKUP_REFRESH_TEXT = '↻ Refresh'
REFRESHED_NOTIFICATION = 'Refreshed!'

LIST_CALLBACK_DATA = 'list'
REFRESH_CALLBACK_DATA = 'refresh'

def lst(update, context):
    user_id = int(update.message.from_user['id'])
    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup()
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def lst_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup()
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def refresh_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    refresh_all_availabilities(user_id)
    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup()
    try:
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception:
        pass
    finally:
        query.answer(REFRESHED_NOTIFICATION)


def _get_books_text(user_id):
    ## Sort by availability first, then title
    def sort_all_book_info(all_book_info):
        return sorted(all_book_info, key=lambda bi: (not bi['is_available'], bi['title']))

    def build_book_text(book_info):
        colour = '🟢' if book_info['is_available'] else '🔴'
        return '%s /%d: %s' % (colour, book_info['bid'], book_info['title'])

    all_book_info = get_all_book_info(user_id)
    all_book_info = sort_all_book_info(all_book_info)
    if not all_book_info:
        text = NO_BOOKS_STRING
    else:
        text = BOOKS_PREFIX + '\n'.join(build_book_text(book_info) for book_info in all_book_info)
    return text

def _get_reply_markup():
    keyboard = [[InlineKeyboardButton(REPLY_MARKUP_REFRESH_TEXT, callback_data=REFRESH_CALLBACK_DATA)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


list_handler = CommandHandler('list', lst)
list_callback_handler = CallbackQueryHandler(lst_callback, pattern='^' + LIST_CALLBACK_DATA + '$')
refresh_callback_handler = CallbackQueryHandler(refresh_callback, pattern='^' + REFRESH_CALLBACK_DATA + '$')
