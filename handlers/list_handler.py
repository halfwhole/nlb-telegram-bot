from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ChatAction
from telegram.ext import CommandHandler, CallbackQueryHandler

from db_helpers import get_all_book_info, refresh_all_availabilities
from handlers import ADD_CALLBACK_DATA, FILTER_CALLBACK_DATA, LIST_CALLBACK_DATA, REFRESH_CALLBACK_DATA

BOOKS_PREFIX = '<b>Books:</b> across all libraries\n'
# TODO: Change NO_BOOKS_STRING to give instructions on how to add a book
NO_BOOKS_STRING = "You currently have no books!\nClick on 'Add Book' to get started."
REFRESHED_NOTIFICATION = 'Refreshed!'

REPLY_MARKUP_REFRESH_TEXT = '↻ Refresh'
REPLY_MARKUP_ADD_BOOK_TEXT = '+ Add Book'
REPLY_MARKUP_FILTER_TEXT = 'Filter by Library'

## TODO: implement filtering by library

def lst(update, context):
    user_id = int(update.message.from_user['id'])
    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup(user_id)
    update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def lst_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup(user_id)
    query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def refresh_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    bot = context.bot
    chat_id = update.effective_message.chat_id

    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    ## TODO: make this non-blocking, timeout?
    refresh_all_availabilities(user_id)

    text = _get_books_text(user_id)
    reply_markup = _get_reply_markup(user_id)
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

def _get_reply_markup(user_id):
    refresh_button = InlineKeyboardButton(REPLY_MARKUP_REFRESH_TEXT, callback_data=REFRESH_CALLBACK_DATA)
    add_book_button = InlineKeyboardButton(REPLY_MARKUP_ADD_BOOK_TEXT, callback_data=ADD_CALLBACK_DATA)
    filter_button = InlineKeyboardButton(REPLY_MARKUP_FILTER_TEXT, callback_data=FILTER_CALLBACK_DATA)
    if not get_all_book_info(user_id):  # User has no books
        keyboard = [[add_book_button]]
    else:
        keyboard = [[refresh_button], [add_book_button, filter_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


list_handler = CommandHandler('list', lst)
list_callback_handler = CallbackQueryHandler(lst_callback, pattern='^' + LIST_CALLBACK_DATA + '$')
refresh_callback_handler = CallbackQueryHandler(refresh_callback, pattern='^' + REFRESH_CALLBACK_DATA + '$')
