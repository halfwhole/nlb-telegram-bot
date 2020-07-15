from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackQueryHandler

from app.db_helpers import get_all_branch_names, get_filter_branch_names, delete_all_filters, toggle_filter
from app.handlers import FILTER_CALLBACK_DATA, FILTER_CLEAR_CALLBACK_DATA, LIST_CALLBACK_DATA

FILTER_HEADER = '<b>Filters:</b>'
NO_FILTERS_HEADER = """
You have no filters! All libraries will be selected by default.
Click on any of the branch names below to toggle its filter.
"""
FILTER_BRANCH_NAME_FORMAT = '• %s'

REPLY_MARKUP_BACK_TEXT = '‹‹ Back to List'
REPLY_MARKUP_CLEAR_TEXT = 'Clear All Filters'

def filter_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    _filter_callback_execute(query, user_id)

def filter_clear_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    delete_all_filters(user_id)
    _filter_callback_execute(query, user_id)

def filter_toggle_callback(update, context):
    query = update.callback_query
    user_id = int(query.message.chat['id'])
    branch_name = query.data.split('_')[-1]
    toggle_filter(user_id, branch_name)
    _filter_callback_execute(query, user_id)

def _filter_callback_execute(query, user_id):
    all_branch_names = get_all_branch_names(user_id)
    reply_markup = _get_reply_markup(all_branch_names)
    filter_branch_names = get_filter_branch_names(user_id)
    if not filter_branch_names:
        text = NO_FILTERS_HEADER
    else:
        text = FILTER_HEADER + '\n' + '\n'.join([FILTER_BRANCH_NAME_FORMAT % x for x in filter_branch_names])

    try:
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except Exception:
        pass
    finally:
        query.answer()


def _get_reply_markup(branch_names):
    back_button = InlineKeyboardButton(REPLY_MARKUP_BACK_TEXT, callback_data=LIST_CALLBACK_DATA)
    clear_button = InlineKeyboardButton(REPLY_MARKUP_CLEAR_TEXT, callback_data=FILTER_CLEAR_CALLBACK_DATA)
    branch_name_buttons = [InlineKeyboardButton(branch_name, callback_data='%s_%s' % (FILTER_CALLBACK_DATA, branch_name)) for branch_name in branch_names]

    paired_branch_name_buttons = [[a, b] for a, b in zip(branch_name_buttons[::2], branch_name_buttons[1::2])]
    if len(branch_name_buttons) % 2 is not 0:
        paired_branch_name_buttons.append([branch_name_buttons[-1]])

    keyboard = [*paired_branch_name_buttons, [back_button, clear_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


filter_callback_handler = CallbackQueryHandler(filter_callback, pattern='^' + FILTER_CALLBACK_DATA + '$')
filter_clear_callback_handler = CallbackQueryHandler(filter_clear_callback, pattern='^' + FILTER_CLEAR_CALLBACK_DATA + '$')
filter_toggle_callback_handler = CallbackQueryHandler(filter_toggle_callback, pattern='^%s_.+$' % FILTER_CALLBACK_DATA)
