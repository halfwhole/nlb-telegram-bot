import telegram
from telegram.ext import CommandHandler

from db_helpers import get_book_info

BOOKS_PREFIX = '*Books*\n'
NO_BOOKS_STRING = 'You have no books!\nUse /add to start adding new books.'

def lst(update, context):
    user_id = int(update.message.from_user['id'])
    book_info = get_book_info(user_id)
    if not book_info:
        update.message.reply_text(NO_BOOKS_STRING)
        return

    text = BOOKS_PREFIX + '\n'.join('• %d: %s' % (bi['bid'], bi['title']) for bi in book_info)
    update.message.reply_text(text, parse_mode=telegram.ParseMode.MARKDOWN_V2)

list_handler = CommandHandler('list', lst)
