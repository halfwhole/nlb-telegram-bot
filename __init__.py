import logging
import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from config import token
from handlers.start_handler import start_handler
from handlers.help_handler import help_handler
from handlers.list_handler import list_handler
from handlers.add_handler import add_handler
from handlers.delete_handler import delete_handler
from handlers.refresh_handler import refresh_handler
from handlers.fallback_handler import fallback_handler

## Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

## Error handlers
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(start_handler)
    dp.add_handler(help_handler)
    dp.add_handler(list_handler)
    dp.add_handler(add_handler)
    dp.add_handler(delete_handler)

    dp.add_handler(refresh_handler)

    dp.add_handler(fallback_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    print("Bot is up and running")
    updater.idle()


if __name__ == '__main__':
    main()
