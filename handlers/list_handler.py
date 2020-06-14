from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler

from db_helpers import get_all_book_info, refresh_all_availabilities
from handlers import ADD_CALLBACK_DATA, LIST_CALLBACK_DATA, REFRESH_CALLBACK_DATA

BOOKS_PREFIX = '<b>Books:</b> across all libraries\n'
NO_BOOKS_STRING = "You currently have no books!\nClick on 'Add Book' to get started."
REFRESHED_NOTIFICATION = 'Refreshed!'

REPLY_MARKUP_REFRESH_TEXT = '↻ Refresh'
REPLY_MARKUP_ADD_TEXT = '+ Add Book'

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
    refresh_button = InlineKeyboardButton(REPLY_MARKUP_REFRESH_TEXT, callback_data=REFRESH_CALLBACK_DATA)
    add_button = InlineKeyboardButton(REPLY_MARKUP_ADD_TEXT, callback_data=ADD_CALLBACK_DATA)
    keyboard = [[refresh_button, add_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


list_handler = CommandHandler('list', lst)
list_callback_handler = CallbackQueryHandler(lst_callback, pattern='^' + LIST_CALLBACK_DATA + '$')
refresh_callback_handler = CallbackQueryHandler(refresh_callback, pattern='^' + REFRESH_CALLBACK_DATA + '$')
