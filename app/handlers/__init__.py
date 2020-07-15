from app.config import token, logger
from app.handlers.start_handler import start_handler
from app.handlers.help_handler import help_handler
from app.handlers.howtoadd_handler import howtoadd_handler
from app.handlers.source_handler import source_handler
from app.handlers.list_handler import list_handler, list_callback_handler, refresh_callback_handler
from app.handlers.filter_handler import filter_callback_handler, filter_clear_callback_handler, filter_toggle_callback_handler
from app.handlers.view_handler import view_handler
from app.handlers.add_handler import add_handler
from app.handlers.delete_handler import delete_callback_handler
from app.handlers.fallback_handler import fallback_handler

def error(update, context):
    ## TODO: Put this into a constant
    logger.warning('ERROR: Update "%s" caused error "%s"', update, context.error)

def setup_handlers(dp):
    ## Putting these above so that typing /list or /start etc. in the midst of the conversation won't sabotage it
    dp.add_handler(add_handler)
    dp.add_handler(delete_callback_handler)

    dp.add_handler(list_handler)
    dp.add_handler(list_callback_handler)
    dp.add_handler(refresh_callback_handler)

    dp.add_handler(filter_callback_handler)
    dp.add_handler(filter_clear_callback_handler)
    dp.add_handler(filter_toggle_callback_handler)

    dp.add_handler(view_handler)

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(howtoadd_handler)
    dp.add_handler(source_handler)

    dp.add_handler(fallback_handler)
    dp.add_error_handler(error)
