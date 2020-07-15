from telegram.ext import CommandHandler

HELP_MESSAGE = """
Welcome to the NLB library bot!
I track the availability of your selected NLB books.
• /list: The main page. Add, delete, view, and refresh books here.
• /howtoadd: Show instructions on how to add a book.
• /source: Show further details about this project.
"""

def help(update, context):
    update.message.reply_text(HELP_MESSAGE)

help_handler = CommandHandler('help', help)
