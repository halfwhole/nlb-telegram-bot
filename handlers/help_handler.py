from telegram.ext import CommandHandler

def help(update, context):
    ## TODO: write a better help message, please
    ## TODO: separate out obnoxious github link into separate credits/source/contributing command
    help_message = """
    You can do the following:
- /start
- /help
- /list
    You can find me at https://github.com/halfwhole/nlb-telegram-bot.
    """
    update.message.reply_text(help_message)

help_handler = CommandHandler('help', help)
