from telegram.ext import MessageHandler, Filters

def four_oh_four(update, context):
    update.message.reply_text("I didn't understand your message '%s'!" % update.message.text)

fallback_handler = MessageHandler(Filters.text, four_oh_four)
