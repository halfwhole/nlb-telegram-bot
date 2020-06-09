import logging
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import conn_string

## Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

## States
ADD_CONTINUE = range(1)

## Command handlers
def start(update, context):
    update.message.reply_text('Hi!')
    print(update.message.from_user['id'])

def help(update, context):
    help_message = """
    You can do the following:
- /start
- /help
- /add
    """
    update.message.reply_text(help_message)

def add_start(update, context):
    update.message.reply_text('What book would you like to add next? Use /end to end at any time.')
    return ADD_CONTINUE

def add_continue(update, context):
    text = update.message.text.strip()
    try:
        book_id = int(text)
        print('Add book with ID %d' % book_id)
        update.message.reply_text('Added book with id %d. What book would you like to add next? Use /end to end at any time.' % book_id)
    except ValueError:
        update.message.reply_text('That was not a valid book ID! Please try again.')
    return ADD_CONTINUE

def add_end(update, context):
    update.message.reply_text('Books added, exiting.')
    return ConversationHandler.END

def four_oh_four(update, context):
    update.message.reply_text("I didn't understand your message '%s'!" % update.message.text)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    add_book_handler = ConversationHandler(
        entry_points = [CommandHandler('add', add_start)],
        states = {
            ADD_CONTINUE: [CommandHandler('end', add_end),
                           MessageHandler(Filters.text, add_continue)]
        },
        fallbacks = [CommandHandler('end', add_end)]
    )
    dp.add_handler(add_book_handler)

    dp.add_handler(MessageHandler(Filters.text, four_oh_four))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    print(engine)
    main()
