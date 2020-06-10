from telegram.ext import CommandHandler

def help(update, context):
    help_message = """
    You can do the following:
- /start
- /help
- /add
    """
    update.message.reply_text(help_message)

help_handler = CommandHandler('help', help)
