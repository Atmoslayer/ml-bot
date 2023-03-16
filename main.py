import os
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)


def detect_intent_texts(project_id, session_id, text):

    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def start(update, context):
    user = update.message.from_user
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        text='Здравствуйте!',
        reply_markup=reply_markup,
    )


def reply(update, context):
    reply_markup = ReplyKeyboardRemove()
    reply_text = detect_intent_texts(project_id, chat_id, update.message.text)
    update.message.reply_text(
        text=reply_text,
        reply_markup=reply_markup,
    )


if __name__ == '__main__':

    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    google_token = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    chat_id = os.getenv('CHAT_ID')
    project_id = os.getenv('PROJECT_ID')
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.all, reply))


    logging.info('The bot started')
    updater.start_polling()
    updater.idle()