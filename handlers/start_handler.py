from telegram.ext import CommandHandler

START_FORMAT = """
Hi, @%s!
Use /list to get started.
For more help, use /help.
"""

def start(update, context):
    username = update.message.from_user['username']
    update.message.reply_text(START_FORMAT % username)

start_handler = CommandHandler('start', start)
