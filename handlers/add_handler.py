from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

from nlb import get_title_details, get_availability_info
from db_helpers import is_book_present, add_book_availabilities

ADD_IN_PROGRESS = range(1)

ADD_BOOK_START_STRING = 'What book ID would you like to add?'
ADDED_BOOK_FORMAT = 'Added "%s".'
INVALID_BID_STRING = 'That book ID was invalid.\nPlease try again, or use /end to finish.'
BOOK_EXISTS_STRING = 'That book already exists.\nPlease try again, or use /end to finish.'
PLEASE_WAIT_STRING = 'Please wait while I gather the book information...'
END_STRING = "You're done with adding books."
RETURN_STRING = 'Use /list to return to the main list.'

ADD_CALLBACK_DATA = 'add'

## TODO: add tons of logging details!

def add_start_callback(update, context):
    query = update.callback_query
    query.edit_message_text(ADD_BOOK_START_STRING)
    return ADD_IN_PROGRESS

def add_in_progress(update, context):
    text = update.message.text.strip()
    if not text.isdigit():
        update.message.reply_text(INVALID_BID_STRING)
        return ADD_IN_PROGRESS
    bid = int(text)
    user_id = int(update.message.from_user['id'])
    return_code = _add_in_progress_execute(bid, user_id, update.message.reply_text)
    return return_code

def add_in_progress_callback(update, context):
    query = update.callback_query
    bid = int(query.data.split('_')[-1])
    user_id = int(query.message.chat['id'])
    return_code = _add_in_progress_execute(bid, user_id, query.edit_message_text)
    return return_code

## Executes the book adding, and sends/edits text appropriately
def _add_in_progress_execute(bid, user_id, send_text_func):
    if is_book_present(bid, user_id):
        send_text_func(BOOK_EXISTS_STRING)
        return ADD_IN_PROGRESS

    sent_message = send_text_func(PLEASE_WAIT_STRING)
    try:
        ## TODO: send_chat_action TYPING?
        ## TODO: make this non-blocking and async. What if other users want to do other things in the meantime?
        ## TODO: implement TIMEOUT
        title_details = get_title_details(bid)
        availability_info = get_availability_info(bid)
    except Exception as e:
        sent_message.edit_text(INVALID_BID_STRING)
        return ADD_IN_PROGRESS

    title = title_details['title']
    add_book_availabilities(bid, user_id, title_details, availability_info)
    sent_message.edit_text(ADDED_BOOK_FORMAT % title + '\n' + RETURN_STRING)
    ## TODO: Go to list handler
    return ConversationHandler.END


def add_end(update, context):
    update.message.reply_text(END_STRING + '\n' + RETURN_STRING)
    ## TODO: Go to list handler
    return ConversationHandler.END


add_handler = ConversationHandler(
    entry_points = [CallbackQueryHandler(add_start_callback, pattern='^%s$' % ADD_CALLBACK_DATA),
                    CallbackQueryHandler(add_in_progress_callback, pattern='^%s_\d+$' % ADD_CALLBACK_DATA)],
    states = {
        ADD_IN_PROGRESS: [CommandHandler('end', add_end), MessageHandler(Filters.text, add_in_progress)]
    },
    fallbacks = [CommandHandler('end', add_end)]
)
