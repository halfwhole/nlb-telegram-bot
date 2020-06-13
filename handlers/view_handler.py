import itertools
from telegram import ParseMode
from telegram.ext import MessageHandler, Filters

from db_helpers import get_book_title_details, get_book_availabilities

BOOK_FORMAT = '<b>Title:</b> %s\n<b>Author:</b> %s'
AVAILABILITY_LIBRARY_HEADER_FORMAT = '<b>%s</b>'
AVAILABILITY_FORMAT = '%s %s, %s\n       %s'
TRIMMED_TEXT = '<i>...additional text has been trimmed to keep within the length limit</i>'
FOOTER_TEXT = 'Use /list to return to the main list.'

def view(update, context):
    def make_text(availabilities):
        texts = []
        for branch_name, group in itertools.groupby(availabilities, lambda a: a['branch_name']):
            group_texts = []
            group_texts.append(AVAILABILITY_LIBRARY_HEADER_FORMAT % branch_name)
            for availability in group:
                colour = '🟢' if availability['is_available'] else '🔴'
                group_texts.append(AVAILABILITY_FORMAT % (colour, availability['shelf_location'], availability['call_number'], availability['status_desc']))
            texts.append('\n'.join(group_texts))
        return '\n'.join(texts)

    def trim_text_if_necessary(text):
        if len(text) <= 4096:
            return text
        trimmed_text = text[:4090 - len(TRIMMED_TEXT) - len(FOOTER_TEXT)]
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
    text += '\n\n' + FOOTER_TEXT

    update.message.reply_text(text, parse_mode=ParseMode.HTML)

view_handler = MessageHandler(Filters.regex('^/\d+$'), view)
