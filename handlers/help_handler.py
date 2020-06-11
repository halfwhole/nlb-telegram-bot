from telegram.ext import CommandHandler

def help(update, context):
    help_message = """
    You can do the following:
- /start
- /help
- /add
- /delete
- /list
    You can find me at https://github.com/halfwhole/nlb-telegram-bot.
    """
    ## TODO: separate out obnoxious github link into separate credits/source/contributing command
    update.message.reply_text(help_message)

help_handler = CommandHandler('help', help)
