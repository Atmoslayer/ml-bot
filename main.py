import os
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)


def start(update, context):
    user = update.message.from_user
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте!',
        reply_markup=reply_markup,
    )


def echo(update, context):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text=update.message.text,
        reply_markup=reply_markup,
    )


if __name__ == '__main__':

    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))


    logging.info('The bot started')
    updater.start_polling()
    updater.idle()