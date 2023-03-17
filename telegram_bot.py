import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from train_network import detect_intent_texts


def start(update, context):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте!',
        reply_markup=reply_markup,
    )


def reply(update, context):
    reply_markup = ReplyKeyboardRemove()
    reply_text, is_fallback = detect_intent_texts(project_id, chat_id, update.message.text)
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    project_id = os.getenv('PROJECT_ID')

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, reply))
    logging.info('TG bot started')
    updater.start_polling()
    updater.idle()

