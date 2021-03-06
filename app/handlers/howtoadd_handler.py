from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction

from app.constants import ADD_CALLBACK_DATA, LIST_CALLBACK_DATA, REPLY_MARKUP_ADD_BOOK_TEXT, REPLY_MARKUP_BACK_TEXT

HOWTOADD_MESSAGE = """
1. Search for your book using the NLB catalogue at catalogue.nlb.gov.sg.
2. Copy the book's URL as shown in the image above.
3. When adding the book using 'Add Book', paste the copied URL.
(Do note that electronic resources are not supported.)
"""
HOWTOADD_PHOTO_FILE = 'assets/howtoadd.png'


def howtoadd(update, context):
    chat_id = update.effective_message.chat_id
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    update.message.reply_photo(open(HOWTOADD_PHOTO_FILE, 'rb'))
    update.message.reply_text(HOWTOADD_MESSAGE, reply_markup=_get_back_reply_markup())

def _get_back_reply_markup():
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    add_book_button = InlineKeyboardButton(REPLY_MARKUP_ADD_BOOK_TEXT, callback_data=ADD_CALLBACK_DATA)
    keyboard = [[back_button, add_book_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

howtoadd_handler = CommandHandler('howtoadd', howtoadd)
