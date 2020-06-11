from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

from db_helpers import delete_book_and_availabilities, get_book_title_details, is_book_present

DELETE_CONTINUE = range(1)

INVALID_BID_STRING = 'That book ID was invalid. Please try again, or use /end to finish.'
BOOK_DOES_NOT_EXIST_STRING = 'No book with the ID exists. Please try again, or use /end to finish.'
DELETE_BOOK_START_STRING = 'What book would you like to delete next? Use /end to finish.'
DELETED_BOOK_STRING = 'Deleted "%s".'
END_STRING = "Books deleted, you're done!"

def delete_start(update, context):
    update.message.reply_text(DELETE_BOOK_START_STRING)
    return DELETE_CONTINUE

def delete_continue(update, context):
    text = update.message.text.strip()
    if not text.isdigit():
        update.message.reply_text(INVALID_BID_STRING)
        return

    bid = int(text)
    user_id = int(update.message.from_user['id'])
    if not is_book_present(bid, user_id):
        update.message.reply_text(BOOK_DOES_NOT_EXIST_STRING)
        return

    title_details = get_book_title_details(bid, user_id)
    title = title_details['title']

    delete_book_and_availabilities(bid, user_id)
    update.message.reply_text(DELETED_BOOK_STRING % title + '\n' + DELETE_BOOK_START_STRING)

    return DELETE_CONTINUE

def delete_end(update, context):
    update.message.reply_text(END_STRING)
    return ConversationHandler.END

delete_handler = ConversationHandler(
    entry_points = [CommandHandler('delete', delete_start)],
    states = {
        DELETE_CONTINUE: [CommandHandler('end', delete_end), MessageHandler(Filters.text, delete_continue)]
    },
    fallbacks = [CommandHandler('end', delete_end)]
)
