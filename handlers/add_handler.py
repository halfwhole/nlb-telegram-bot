from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from nlb import get_title_details, get_availability_info
from db_helpers import is_book_present, add_book_availabilities_db

ADD_CONTINUE = range(1)

ADD_BOOK_START_STRING = 'What book ID would you like to add next? Use /end to finish.'
ADDED_BOOK_STRING = 'Added "%s".'
INVALID_BID_STRING = 'That book ID was invalid. Please try again, or use /end to finish.'
BOOK_EXISTS_STRING = 'That book already exists. Please try again, or use /end to finish.'
PLEASE_WAIT_STRING = 'Please wait while I gather the book information...'
END_STRING = "Books added, you're done!"

## TODO: add tons of logging details!

def add_start(update, context):
    update.message.reply_text(ADD_BOOK_START_STRING)
    return ADD_CONTINUE

def add_continue(update, context):
    text = update.message.text.strip()
    if not text.isdigit():
        update.message.reply_text(INVALID_BID_STRING)
        return

    bid = int(text)
    user_id = int(update.message.from_user['id'])
    if is_book_present(bid, user_id):
        update.message.reply_text(BOOK_EXISTS_STRING)
        return

    try:
        update.message.reply_text(PLEASE_WAIT_STRING)
        title_details = get_title_details(bid)
        availability_info = get_availability_info(bid)
    except Exception as e:
        update.message.reply_text(INVALID_BID_STRING)
        return

    title = title_details['title']
    add_book_availabilities_db(bid, user_id, title_details, availability_info)
    update.message.reply_text(ADDED_BOOK_STRING % title + '\n' + ADD_BOOK_START_STRING)

    return ADD_CONTINUE

def add_end(update, context):
    update.message.reply_text(END_STRING)
    return ConversationHandler.END

add_handler = ConversationHandler(
    entry_points = [CommandHandler('add', add_start)],
    states = {
        ADD_CONTINUE: [CommandHandler('end', add_end), MessageHandler(Filters.text, add_continue)]
    },
    fallbacks = [CommandHandler('end', add_end)]
)
