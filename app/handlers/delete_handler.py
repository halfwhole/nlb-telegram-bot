from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

from app.db_helpers import delete_book_and_availabilities, delete_hanging_filters, get_book_title_details, is_book_present
from app.constants import ADD_CALLBACK_DATA, DELETE_CALLBACK_DATA, LIST_CALLBACK_DATA, REPLY_MARKUP_BACK_TEXT, REPLY_MARKUP_UNDO_TEXT

BOOK_DOES_NOT_EXIST_STRING = 'The book does not exist.'
DELETED_BOOK_STRING = 'Deleted "%s".'


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
    delete_hanging_filters(user_id)

    text = DELETED_BOOK_STRING % title
    reply_markup = _get_reply_markup(bid)
    query.edit_message_text(text, reply_markup=reply_markup)
    query.answer()

def _get_reply_markup(bid):
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    undo_button = InlineKeyboardButton(REPLY_MARKUP_UNDO_TEXT, callback_data=ADD_CALLBACK_DATA + '_' + str(bid))
    keyboard = [[back_button, undo_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
   

delete_callback_handler = CallbackQueryHandler(delete_callback, pattern='^%s_\d+$' % DELETE_CALLBACK_DATA)
