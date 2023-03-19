import os
import logging
import random
import vk_api

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from train_network import detect_intent_texts


class BotLogsHandler(logging.Handler):

    def __init__(self, admin_chat_id, vk_api):
        self.admin_chat_id = admin_chat_id
        self.vk_api = vk_api
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        self.vk_api.messages.send(
            user_id=self.admin_chat_id,
            message=log_entry,
            random_id=random.randint(1, 1000)
        )


def vk_bot_start(vk_api, vk_session, project_id, logger):
    longpoll = VkLongPoll(vk_session)
    logger.info('VK bot started')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, project_id)


def reply(event, vk_api, project_id):
    chat_id = event.user_id
    reply_text, is_fallback = detect_intent_texts(project_id, chat_id, event.text)
    if not is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_text,
            random_id=random.randint(1,1000)
        )


def main(vk_api):
    logger = logging.getLogger('bot_logger')

    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    admin_chat_id = os.getenv('VK_ADMIN_CHAT_ID')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    logger.setLevel(logging.INFO)
    log_handler = BotLogsHandler(admin_chat_id, vk_api)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)

    logger.addHandler(log_handler)

    vk_bot_start(vk_api, vk_session, project_id, logger)


if __name__ == '__main__':
    main(vk_api)