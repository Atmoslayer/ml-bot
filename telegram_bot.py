import logging
import os
import telegram

from functools import partial
from dotenv import load_dotenv
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from train_network import detect_intent_texts

logger = logging.getLogger('bot_logger')

class BotLogsHandler(logging.Handler):

    def __init__(self, bot, admin_chat_id):
        self.bot = bot
        self.admin_chat_id = admin_chat_id
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=self.admin_chat_id,
            text=log_entry,
        )


def start(update, context):
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте!',
        reply_markup=reply_markup,
    )


def reply(update, context, project_id):
    chat_id = update.message.from_user.id
    reply_markup = ReplyKeyboardRemove()
    reply_text, is_fallback = detect_intent_texts(project_id, chat_id, update.message.text)
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup,
    )


def main():
    load_dotenv()
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    bot = telegram.Bot(token=tg_bot_token)
    admin_chat_id = os.getenv('TG_ADMIN_CHAT_ID')
    project_id = os.getenv('PROJECT_ID')

    logger.setLevel(logging.INFO)
    log_handler = BotLogsHandler(bot, admin_chat_id)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)

    logger.addHandler(log_handler)

    updater = Updater(token=tg_bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, partial(reply, project_id=project_id)))
    logger.info('The bot started')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
   main()
