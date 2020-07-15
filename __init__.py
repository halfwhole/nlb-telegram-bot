import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from app.config import token, logger
from app.handlers import setup_handlers

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    setup_handlers(dp)
    updater.start_polling()
    ## TODO: Put this into a constant
    logger.info('START: Bot is up and running')
    updater.idle()


if __name__ == '__main__':
    main()
