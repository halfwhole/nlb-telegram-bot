import itertools
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import MessageHandler, Filters

from handlers.list_handler import LIST_CALLBACK_DATA
from handlers.delete_handler import DELETE_CALLBACK_DATA
from db_helpers import get_book_title_details, get_book_availabilities

BOOK_FORMAT = '<b>Title:</b> %s\n<b>Author:</b> %s'
AVAILABILITY_LIBRARY_HEADER_FORMAT = '<b>%s</b>'
AVAILABILITY_FORMAT = '%s %s\n       %s\n       %s'
TRIMMED_TEXT = '<i>...additional text has been trimmed to keep within the length limit</i>'

REPLY_MARKUP_BACK_TEXT = '‹‹ Back to List'
REPLY_MARKUP_DELETE_TEXT = 'Delete Book'

def view(update, context):
    def make_text(availabilities):
        def make_group_text(availability):
            return AVAILABILITY_FORMAT % (
                '🟢' if availability['is_available'] else '🔴',
                availability['status_desc']    if availability['status_desc']    else '<i>&lt;No status description&gt;</i>',
                availability['shelf_location'] if availability['shelf_location'] else '<i>&lt;No shelf location&gt;</i>',
                availability['call_number']    if availability['call_number']    else '<i>&lt;No call number&gt;</i>'
            )
        texts = []
        for branch_name, group in itertools.groupby(availabilities, lambda a: a['branch_name']):
            group_text_header = AVAILABILITY_LIBRARY_HEADER_FORMAT % branch_name
            group_text_availabilities = '\n'.join([make_group_text(availability) for availability in group])
            texts.append(group_text_header + '\n' + group_text_availabilities)
        return '\n'.join(texts)

    def trim_text_if_necessary(text):
        if len(text) <= 4096:
            return text
        trimmed_text = text[:4090 - len(TRIMMED_TEXT)]
        trimmed_text = '\n'.join(trimmed_text.splitlines()[:-1]) # Remove last line: it might be incomplete, giving unclosed HTML tags
        return trimmed_text + '\n' + TRIMMED_TEXT

    bid = int(update.message.text[1:])  # Remove leading '/'
    user_id = int(update.message.from_user['id'])

    title_details = get_book_title_details(bid, user_id)
    availabilities = get_book_availabilities(bid, user_id)

    available_availabilities = filter(lambda a: a['is_available'], availabilities)
    unavailable_availabilities = filter(lambda a: not a['is_available'], availabilities)

    book_text = BOOK_FORMAT % (title_details['title'], title_details['author'])
    available_group_text = make_text(available_availabilities)
    unavailable_group_text = make_text(unavailable_availabilities)

    text = book_text + '\n\n' + (available_group_text + '\n' if available_group_text else '') + unavailable_group_text
    text = trim_text_if_necessary(text)
    reply_markup = _get_reply_markup(bid)

    update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


def _get_reply_markup(bid):
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    delete_button = InlineKeyboardButton(REPLY_MARKUP_DELETE_TEXT, callback_data=DELETE_CALLBACK_DATA + '_' + str(bid))
    keyboard = [[back_button, delete_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


view_handler = MessageHandler(Filters.regex('^/\d+$'), view)
