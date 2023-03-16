import vk_api
import os
import logging
import random

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from main import detect_intent_texts


def reply(event, vk_api, project_id):
    chat_id = event.user_id
    reply_text = detect_intent_texts(project_id, chat_id, event.text)

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply_text,
        random_id=random.randint(1,1000)
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    google_token = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
    project_id = os.getenv('PROJECT_ID')

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk_api, project_id)