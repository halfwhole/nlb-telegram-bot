from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters

## States
ADD_CONTINUE = range(1)

def add_start(update, context):
    update.message.reply_text('What book would you like to add next? Use /end to end at any time.')
    return ADD_CONTINUE

def add_continue(update, context):
    text = update.message.text.strip()
    user_id = update.message.from_user['id']
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

add_handler = ConversationHandler(
    entry_points = [CommandHandler('add', add_start)],
    states = {
        ADD_CONTINUE: [CommandHandler('end', add_end), MessageHandler(Filters.text, add_continue)]
    },
    fallbacks = [CommandHandler('end', add_end)]
)
