import argparse
import os
import logging
import vk_api

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vk_bot import vk_bot_start
from train_network import train_network
from telegram_bot import start_tg_bot


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Bots options parser')
    parser.add_argument('--questions_path', help='Enter path to access questions json file', type=str,
                        default='questions')
    parser.add_argument('-tg', '--run_telegram_bot', help='Run telegram bot', action='store_true')
    parser.add_argument('-vk', '--run_vk_bot', help='Run vk bot', action='store_true')
    parser.add_argument('-tr', '--run_network_training', help='Run neural network training', action='store_true')
    arguments = parser.parse_args()

    questions_path = arguments.questions_path
    run_telegram_bot = arguments.run_telegram_bot
    run_vk_bot = arguments.run_vk_bot
    run_network_training = arguments.run_network_training

    load_dotenv()
    google_token = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    project_id = os.getenv('PROJECT_ID')

    if run_network_training:
        train_network(questions_path, project_id)

    if run_vk_bot:
        vk_bot_start(vk_api)

    if run_telegram_bot:
        start_tg_bot()
