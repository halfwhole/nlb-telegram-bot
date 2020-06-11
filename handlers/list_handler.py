from telegram.ext import CommandHandler

from db_helpers import get_book_info

def lst(update, context):
    user_id = int(update.message.from_user['id'])
    book_info = get_book_info(user_id)
    text = '\n'.join('%d: %s' % (bi['bid'], bi['title']) for bi in book_info)
    update.message.reply_text(text)

list_handler = CommandHandler('list', lst)
