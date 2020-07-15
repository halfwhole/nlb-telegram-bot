from telegram.ext import CommandHandler

SOURCE_MESSAGE = 'You can visit this project at https://github.com/halfwhole/nlb-telegram-bot.'

def source(update, context):
    update.message.reply_text(SOURCE_MESSAGE)

source_handler = CommandHandler('source', source)
