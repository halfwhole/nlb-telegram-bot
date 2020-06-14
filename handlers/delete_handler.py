from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from db_helpers import delete_book_and_availabilities, get_book_title_details, is_book_present
from handlers.list_handler import LIST_CALLBACK_DATA
from handlers.add_handler import ADD_CALLBACK_DATA

DELETE_CALLBACK_DATA = 'delete'

BOOK_DOES_NOT_EXIST_STRING = 'No book with the ID exists.\nPlease try again, or use /end to finish.'
DELETED_BOOK_STRING = 'Deleted "%s".'

REPLY_MARKUP_BACK_TEXT = '‹‹ Back to List'
REPLY_MARKUP_UNDO_TEXT = 'Undo'


def delete_callback(update, context):
    query = update.callback_query
    bid = int(query.data.split('_')[-1])
    user_id = int(query.message.chat['id'])

    if not is_book_present(bid, user_id):
        update.message.reply_text(BOOK_DOES_NOT_EXIST_STRING)
        return

    title_details = get_book_title_details(bid, user_id)
    title = title_details['title']

    delete_book_and_availabilities(bid, user_id)

    text = DELETED_BOOK_STRING % title
    reply_markup = _get_reply_markup(bid)
    query.edit_message_text(text, reply_markup=reply_markup)

def _get_reply_markup(bid):
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    undo_button = InlineKeyboardButton(REPLY_MARKUP_UNDO_TEXT, callback_data=ADD_CALLBACK_DATA + '_' + str(bid))
    keyboard = [[back_button, undo_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
   

delete_callback_handler = CallbackQueryHandler(delete_callback, pattern='^%s_\d+$' % DELETE_CALLBACK_DATA)
