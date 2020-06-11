from telegram.ext import CommandHandler

from db_helpers import get_book_info

NO_BOOKS_STRING = 'You have no books! Use /add to start adding some.'

def lst(update, context):
    user_id = int(update.message.from_user['id'])
    book_info = get_book_info(user_id)
    text = '\n'.join('%d: %s' % (bi['bid'], bi['title']) for bi in book_info)
    if not text:
        update.message.reply_text(NO_BOOKS_STRING)
        return

    update.message.reply_text(text)

list_handler = CommandHandler('list', lst)
