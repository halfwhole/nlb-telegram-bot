from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

from nlb import get_title_details, get_availability_info
from db_helpers import is_book_present, add_book_availabilities
from handlers import ADD_CALLBACK_DATA, LIST_CALLBACK_DATA


ADD_IN_PROGRESS = range(1)

ADD_BOOK_START_STRING = 'What book URL would you like to add?'
ADDED_BOOK_FORMAT = 'Added "%s".'
INVALID_BID_STRING = 'That book URL is invalid.'
BOOK_ALREADY_EXISTS_STRING = 'That book already exists.'
PLEASE_WAIT_STRING = 'Please wait while I gather the book information...'
END_STRING = "You're done with adding books."

REPLY_MARKUP_BACK_TEXT = '‹‹ Back to List'


def add_start_callback(update, context):
    query = update.callback_query
    query.edit_message_text(ADD_BOOK_START_STRING)
    return ADD_IN_PROGRESS

def add_in_progress(update, context):
    text = update.message.text.strip()
    ## Parse input text: either a book bid or catalogue URL
    try:
        if text.isdigit():
            bid = int(text)
        else:
            bid = int(text.split('/')[-1].split(',')[0])
    except:
        update.message.reply_text(INVALID_BID_STRING, reply_markup=_get_back_reply_markup())
        return ConversationHandler.END
    user_id = int(update.message.from_user['id'])
    chat_id = update.effective_message.chat_id
    return_code = _add_in_progress_execute(bid, user_id, context.bot, chat_id, update.message.reply_text)
    return return_code

def add_in_progress_callback(update, context):
    query = update.callback_query
    bid = int(query.data.split('_')[-1])
    user_id = int(query.message.chat['id'])
    chat_id = update.effective_message.chat_id
    return_code = _add_in_progress_execute(bid, user_id, context.bot, chat_id, query.edit_message_text)
    return return_code

## Executes the book adding, and sends/edits text appropriately
def _add_in_progress_execute(bid, user_id, bot, chat_id, send_text_func):
    if is_book_present(bid, user_id):
        send_text_func(BOOK_ALREADY_EXISTS_STRING, reply_markup=_get_back_reply_markup())
        return ConversationHandler.END

    sent_message = send_text_func(PLEASE_WAIT_STRING)
    try:
        bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        ## TODO: make this non-blocking, timeout?
        title_details = get_title_details(bid)
        availability_info = get_availability_info(bid)
    except Exception as e:
        sent_message.edit_text(INVALID_BID_STRING, reply_markup=_get_back_reply_markup())
        return ConversationHandler.END

    title = title_details['title']
    add_book_availabilities(bid, user_id, title_details, availability_info)
    sent_message.edit_text(ADDED_BOOK_FORMAT % title, reply_markup=_get_back_reply_markup())
    return ConversationHandler.END


def add_end_callback(update, context):
    query = update.callback_query
    query.edit_message_text(END_STRING, reply_markup=_get_back_reply_markup())
    query.answer()
    return ConversationHandler.END


def _get_back_reply_markup():
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


add_handler = ConversationHandler(
    entry_points = [CallbackQueryHandler(add_start_callback, pattern='^%s$' % ADD_CALLBACK_DATA),
                    CallbackQueryHandler(add_in_progress_callback, pattern='^%s_\d+$' % ADD_CALLBACK_DATA)],
    states = {
        ADD_IN_PROGRESS: [MessageHandler(Filters.text, add_in_progress)]
    },
    fallbacks = []
)
